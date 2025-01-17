from datetime import datetime, timedelta
import time
import redis
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse,redirect
from psycopg2 import OperationalError
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from opulaadmin.models import *
from .serializers import *
from rest_framework.exceptions import NotFound
import uuid
from django.db import connections
from cryptography.fernet import Fernet
from .utils import encrypt_password 
import base64
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
# Create your views here.

class TenantAuthView(generics.ListAPIView):
    serializer_class = AuthenticationSerializer

    @swagger_auto_schema(
        operation_description="Retrieve users by role and tenant information",
        responses={200: AuthenticationSerializer},
        manual_parameters=[openapi.Parameter('role', openapi.IN_PATH, description="Role ID to filter users", type=openapi.TYPE_STRING)],
    )

    def get_queryset(self):
        roles = self.kwargs.get("role")
        
        try:
            getroles = RoleManagementModel.objects.get(id=roles)
          
        except RoleManagementModel.DoesNotExist:
            return AuthenticationModel.objects.none() 

        queryset = AuthenticationModel.objects.filter(am_role=getroles)
       
        return queryset.select_related('am_role') 
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = []
        for auth in queryset:
            tenant = TenantModel.objects.filter(tm_auth=auth.id).first() 
            domain_name = tenant.tm_domain_name if tenant else None  
            db_name = tenant.tm_db_name if tenant else None  
            db_user = tenant.tm_db_user if tenant else None  
            db_password = tenant.tm_db_password if tenant else None  

            fernet = Fernet(settings.FERNET_KEY)
            decrypted_password = fernet.decrypt(db_password.encode()).decode()


            data.append({
                "id": auth.id,
                "email": auth.email,
                "tm_db_name": db_name,
                "tm_db_user": db_user,
                "tm_db_password": decrypted_password,
                "tm_domain_name": domain_name,

            })

        return Response({
            "status": 200,
            "message": "Data Retrieved Successfully",
            "data": data
        }, status=status.HTTP_200_OK)



class RoleView(generics.ListAPIView):
    serializer_class = RoleSerializer
    queryset = RoleManagementModel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": 200,
            "message": "Data Retrieved Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
def get_tokens_for_user(user):
   
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }


class TenantRegistrationView(APIView):

    
    def get_redis_client(self):
        return redis.StrictRedis.from_url(settings.REDIS_URL)

    @swagger_auto_schema(
        operation_description="Create a new authentication record",
        request_body=AuthenticationSerializer,
        responses={201: openapi.Response('Authentication record created successfully', AuthenticationSerializer)},
    )
    def create_authentication_model(self, user_data):
        static_role = RoleManagementModel.objects.get(id=2) 
        user = get_user_model().objects.create_user(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password'],
            am_mobile_no=user_data['am_mobile_no'],
            am_role=static_role
        )
        user.set_password(user_data['password'])
        user.save()
        return user

    @swagger_auto_schema(
        operation_description="Create a new tenant record",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'tm_domain_name': openapi.Schema(type=openapi.TYPE_STRING, description='Tenant domain name'),
            }
        ),
        responses={201: openapi.Response('Tenant created successfully', TenantSerializer)},
    )
    def create_tenant_model(self, user, tenant_data, password):
        email_prefix = user.email.split('@')[0]
        domain_name = user.email.split('@')[1].split('.')[0]
        tm_db_user = email_prefix + domain_name

        tenant_data.update({
            'tm_auth': user.id,
            'tm_db_name': f"{user.first_name.lower()}_{str(uuid.uuid4()).replace('-', '')}",
            'tm_db_user': tm_db_user,
            'tm_db_password': Fernet(settings.FERNET_KEY).encrypt(password.encode()).decode(),
        })

        tenant_serializer = TenantSerializer(data=tenant_data)
        if tenant_serializer.is_valid():
            tenant_serializer.save()
            return tenant_serializer.data
        else:
            return None

    @swagger_auto_schema(
        operation_description="Register a new user and tenant",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='Confirm password'),
                'am_mobile_no': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile number'),
                'tm_domain_name': openapi.Schema(type=openapi.TYPE_STRING, description='Tenant domain name'),
            }
        ),
        responses={
            201: openapi.Response('User and tenant created successfully'), 
            400: openapi.Response('Validation failed')  
        }
    )
    def post(self, request, *args, **kwargs):
        auth_serializer = AuthenticationSerializer(data=request.data)

        if auth_serializer.is_valid():
            user_data = auth_serializer.validated_data

            user = self.create_authentication_model(user_data)

            tokens = get_tokens_for_user(user)

            redis_client = self.get_redis_client()
            redis_client.setex(f"user:{user.id}:email", settings.JWT_TOKEN_LIFETIME, user.email)
            redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, tokens['access_token'])
            redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, tokens['refresh_token'])
            redis_client.setex(f"user:{user.id}:id", settings.JWT_TOKEN_LIFETIME, user.id)

            tenant_data = {
                'tm_domain_name': request.data.get('tm_domain_name', ''),
            }
            tenant = self.create_tenant_model(user, tenant_data, request.data['password'])

            if tenant:
                response = JsonResponse({
                    'status': 201,
                    'message': 'User and Tenant created successfully',
                    'token': tokens, 
                }, status=201)

                response.set_cookie('jwt_access_token', tokens['access_token'], httponly=True, secure=settings.SECURE_COOKIES, samesite='Strict', max_age=settings.JWT_TOKEN_LIFETIME)
                response.set_cookie('jwt_refresh_token', tokens['refresh_token'], httponly=True, secure=settings.SECURE_COOKIES, samesite='Strict', max_age=settings.JWT_REFRESH_TOKEN_LIFETIME)

                return response
            else:
                return JsonResponse({'error': 'Failed to create tenant.'}, status=400)

        return JsonResponse(auth_serializer.errors, status=400)




# class TenantRegistrationView(APIView):

#     @swagger_auto_schema(
#         operation_description="Create a new authentication record",
#         request_body=AuthenticationSerializer,
#         responses={201: openapi.Response('Authentication record created successfully', AuthenticationSerializer)},
#     )
#     def create_authentication_model(self, user_data):
#         static_role = RoleManagementModel.objects.get(id=2)
#         user = AuthenticationModel(
#             email=user_data['email'],
#             first_name=user_data['first_name'],
#             last_name=user_data['last_name'],
#             password=user_data['password'],
#             am_mobile_no=user_data['am_mobile_no'],
#             am_role=static_role
#         )
#         user.set_password(user_data['password'])
#         user.save()
#         return user

#     @swagger_auto_schema(
#         operation_description="Create a new tenant record",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'tm_domain_name': openapi.Schema(type=openapi.TYPE_STRING, description='Tenant domain name'),
#             }
#         ),
#         responses={201: openapi.Response('Tenant created successfully', TenantSerializer)},
#     )
#     def create_tenant_model(self, user, tenant_data, password):
#         email_prefix = user.email.split('@')[0]
#         domain_name = user.email.split('@')[1].split('.')[0]
#         tm_db_user = email_prefix + domain_name

#         tenant_data.update({
#             'tm_auth': user.id,
#             'tm_db_name': f"{user.first_name.lower()}_{str(uuid.uuid4()).replace('-', '')}",
#             'tm_db_user': tm_db_user,
#             'tm_db_password': Fernet(settings.FERNET_KEY).encrypt(password.encode()).decode(),
#         })

#         tenant_serializer = TenantSerializer(data=tenant_data)
#         if tenant_serializer.is_valid():
#             tenant_serializer.save()
#             return tenant_serializer.data
#         else:
#             return None

#     @swagger_auto_schema(
#         operation_description="Register a new user and tenant",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
#                 'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
#                 'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
#                 'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
#                 'am_mobile_no': openapi.Schema(type=openapi.TYPE_STRING, description='User mobile number'),
#                 'tm_domain_name': openapi.Schema(type=openapi.TYPE_STRING, description='Tenant domain name'),
#             }
#         ),
#         responses={
#             201: openapi.Response('User and tenant created successfully'), 
#             400: openapi.Response('Validation failed')  
#         }
#     )
#     def post(self, request, *args, **kwargs):
#         auth_serializer = AuthenticationSerializer(data=request.data)

#         with connections['default'].cursor() as cursor:
#             cursor.execute("SET search_path TO admin_management;")

#         if auth_serializer.is_valid():
#             user_data = auth_serializer.validated_data

#             user = self.create_authentication_model(user_data)

           
#             tenant_data = {
#                 'tm_domain_name': request.data.get('tm_domain_name', ''),
#             }
#             tenant = self.create_tenant_model(user, tenant_data, request.data['password'])

#             if tenant:
#                 tokens = get_tokens_for_user(user)

#                 response = Response({
#                     "status": 201,
#                     'message': 'User and Tenant created successfully',
#                     'tokens': tokens 
#                 }, status=status.HTTP_201_CREATED)

#                 response.set_cookie(
#                     key='jwt_access_token',
#                     value=tokens['access_token'],
#                     httponly=True,  
#                     secure=settings.SECURE_COOKIES,  
#                     samesite='Strict',  
#                     max_age=settings.JWT_TOKEN_LIFETIME  ,
#                     # expires=datetime.date.time() + settings.JWT_TOKEN_LIFETIME
#                 )

#                 response.set_cookie(
#                     key='jwt_refresh_token',
#                     value=tokens['refresh_token'],
#                     httponly=True,  
#                     secure=settings.SECURE_COOKIES, 
#                     samesite='Strict',  
#                     max_age=settings.JWT_REFRESH_TOKEN_LIFETIME  
#                 )

#                 return response
#             else:
#                 return Response({'error': 'Failed to create tenant.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TenantLoginView(APIView):

    def get_redis_client(self):
       
        return redis.StrictRedis.from_url(settings.REDIS_URL)

    @swagger_auto_schema(
        operation_description="Login a user and return access & refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            }
        ),
        responses={
            200: openapi.Response('Login successful', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access Token'),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh Token'),
            })),
            400: openapi.Response('Invalid credentials'),
            401: openapi.Response('Unauthorized'),
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            access_token = request.COOKIES.get('access_token')
            refresh = request.COOKIES.get('refresh_token')

         
            redis_client = self.get_redis_client()
        

            access_token_key = f"user:{user.id}:access_token"
            refresh_token_key = f"user:{user.id}:refresh_token"

            print(f"Checking Redis for keys: {access_token_key}, {refresh_token_key}")

            access_token = redis_client.get(access_token_key)
            refresh_token = redis_client.get(refresh_token_key)

        
            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")

       
            if access_token and refresh_token:
                return self.handle_valid_tokens(redis_client, user, access_token.decode('utf-8'), refresh_token.decode('utf-8'))

            elif refresh_token:
                return self.refresh_tokens(redis_client, user, refresh_token.decode('utf-8'))

            else:
                return self.generate_and_store_new_tokens(redis_client, user)

        else:
            return JsonResponse({'error': 'Invalid email or password.'}, status=400)

    def handle_valid_tokens(self, redis_client, user, access_token, refresh_token):
     
        return JsonResponse({
            "status":200,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    def refresh_tokens(self, redis_client, user, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            if refresh:
                user_id = refresh['user_id']
                if user.id != user_id:
                    return JsonResponse({'error': 'Invalid user'}, status=400)

                new_access_token = str(refresh.access_token)
                new_refresh_token = str(refresh)
                
                redis_client = self.get_redis_client()

                redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, new_access_token)
                redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, new_refresh_token)

                return JsonResponse({
                    "status": 200,
                    'message': 'Tokens refreshed successfully',
                    'access_token': new_access_token,
                    'refresh_token': new_refresh_token
                })

            return JsonResponse({'error': 'Invalid refresh token'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Error refreshing tokens'}, status=500)

    def generate_and_store_new_tokens(self, redis_client, user):
        """Generate new access and refresh tokens if no valid tokens are found"""
        try:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            redis_client = self.get_redis_client()

            redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, access_token)
            redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, refresh_token)

            return JsonResponse({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        except Exception as e:
            return JsonResponse({'error': 'Error generating tokens'}, status=500)
    
    def get(self, request, *args, **kwargs):
        redis_client = self.get_redis_client()
        access_token = redis_client.get(f"user:{request.user.id}:access_token")
        refresh_token = redis_client.get(f"user:{request.user.id}:refresh_token")

        if access_token and refresh_token:
            return self.refresh_tokens(request, access_token.decode('utf-8'), refresh_token.decode('utf-8'))

        return JsonResponse({'error': 'No valid tokens found. Please log in again.'}, status=401)




# class TenantLoginView(APIView):
#     # permission_classes = [IsAuthenticated]
#     # authentication_classes = [JWTAuthentication] 

#     def get(self, request, *args, **kwargs):

#         access_token = request.COOKIES.get('jwt_access_token')
#         refresh_token = request.COOKIES.get('jwt_refresh_token')

#         if access_token and refresh_token:
#             return self.refresh_tokens(request, access_token, refresh_token)
        
#         return JsonResponse({
#             'error': 'No valid tokens found. Please log in again.'
#         }, status=401)

#     def refresh_tokens(self, request, access_token, refresh_token):
      
#         try:
#             refresh = RefreshToken(refresh_token)
#             if refresh:
#                 user_id = refresh['user_id']
#                 try:
#                     user = get_user_model().objects.get(id=user_id)
#                 except get_user_model().DoesNotExist:
#                     return JsonResponse({'error': 'User not found'}, status=404)

#                 new_access_token = str(refresh.access_token)
#                 new_refresh_token = str(refresh)

#                 response = JsonResponse({
#                     'message': 'Tokens refreshed successfully',
#                     'access_token': new_access_token,
#                     'refresh_token': new_refresh_token,
#                 })

#                 response.set_cookie(
#                     'jwt_access_token',
#                     new_access_token,
#                     httponly=True,
#                     secure=settings.SECURE_COOKIES,  
#                     samesite='Strict',
#                     max_age=settings.JWT_TOKEN_LIFETIME,
#                     expires=datetime.now() + timedelta(seconds=settings.JWT_TOKEN_LIFETIME)
#                 )

#                 response.set_cookie(
#                     'jwt_refresh_token',
#                     new_refresh_token,
#                     httponly=True,
#                     secure=settings.SECURE_COOKIES,
#                     samesite='Strict',
#                     max_age=settings.JWT_REFRESH_TOKEN_LIFETIME,
#                     expires=datetime.now() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
#                 )

#                 return response
#             else:
#                 return JsonResponse({'error': 'Invalid refresh token'}, status=400)

#         except Exception as e:
#             print(f"Error during token refresh: {e}")
#             return JsonResponse({'error': 'Error refreshing tokens'}, status=500)

#     def post(self, request, *args, **kwargs):
       
#         email = request.data.get('email')
#         password = request.data.get('password')

        
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)

            
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)

#             response = JsonResponse({
#                 'message': 'Login successful',
#                 'access_token': access_token,
#                 'refresh_token': refresh_token,
#             })

#             response.set_cookie(
#                 'jwt_access_token',
#                 access_token,
#                 httponly=True,
#                 secure=settings.SECURE_COOKIES,
#                 samesite='Strict',
#                 max_age=settings.JWT_TOKEN_LIFETIME,
#                 expires=datetime.now() + timedelta(seconds=settings.JWT_TOKEN_LIFETIME)
#             )

#             response.set_cookie(
#                 'jwt_refresh_token',
#                 refresh_token,
#                 httponly=True,
#                 secure=settings.SECURE_COOKIES,
#                 samesite='Strict',
#                 max_age=settings.JWT_REFRESH_TOKEN_LIFETIME,
#                 expires=datetime.now() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
#             )

#             try:
#                 tenant = TenantModel.objects.get(tm_auth=user)
#                 tenant_prefix = tenant.tm_domain_name
#                 tenant_url = f"http://{tenant_prefix}.{settings.OPULA_DOMAIN}/dashboard"
#                 # return redirect(tenant_url)
#                 return Response({"status":200, "message":"Data Retrieve Successfully", "data": tenant_url})
#             except TenantModel.DoesNotExist:
#                 return JsonResponse({'error': 'Tenant information not found.'}, status=404)
#         else:
#             return JsonResponse({'error': 'Invalid email or password.'}, status=400)



class TermsAndConditionView(APIView):
    serializer_class = TermsAndConditionSerializer

    StandardResponseSchema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    )

    @swagger_auto_schema(
        operation_description="Retrieve a list of terms and conditions or a specific one by ID",
        responses={
            200: openapi.Response(
                description="Terms and conditions retrieved successfully", 
                schema=StandardResponseSchema
            ),
            404: openapi.Response(
                description="Term and Condition not found"
            ),
        },
    )
    def get(self, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                term_model_obj = TermsAndConditionmodel.objects.get(pk=kwargs['pk'])
            except TermsAndConditionmodel.DoesNotExist:
                raise NotFound("Term and Condition not found")
            serializer = self.serializer_class(term_model_obj)
            return Response({
                "status": 200,
                "message": "Data Retrieved Successfully",
                "data": serializer.data 
            })
        
        term_model_obj = self.get_queryset()
        serializer = self.serializer_class(term_model_obj, many=True)
        return Response({
            "status": 200,
            "message": "Data Retrieved Successfully",
            "data": serializer.data  
        })

    def get_queryset(self):
        return TermsAndConditionmodel.objects.all()

    @swagger_auto_schema(
        operation_description="Create a new Term and Condition",
        request_body=TermsAndConditionSerializer, 
        responses={
            201: openapi.Response(
                description="Term and Condition created successfully", 
                schema=StandardResponseSchema
            ),
            400: openapi.Response(
                description="Validation failed"
            ),
        }
    )
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        
        if serializer.is_valid():
            serializer.save() 
            return Response({
                "status": 201,
                "message": "Term and Condition Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors  
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing Term and Condition",
        request_body=TermsAndConditionSerializer,  
        responses={
            200: openapi.Response(
                description="Term and Condition updated successfully", 
                schema=StandardResponseSchema
            ),
            400: openapi.Response(
                description="Validation failed"
            ),
            404: openapi.Response(
                description="Term and Condition not found"
            ),
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Term and Condition ID", type=openapi.TYPE_INTEGER)]
    )
    def put(self, *args, **kwargs):
        try:
            instance = TermsAndConditionmodel.objects.get(pk=kwargs['pk'])
        except TermsAndConditionmodel.DoesNotExist:
            raise NotFound("Term and Condition not found")
        
        serializer = self.serializer_class(instance, data=self.request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Term and Condition Updated Successfully",
                "data": serializer.data 
            })
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors  
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing Term and Condition",
        request_body=TermsAndConditionSerializer, 
        responses={
            200: openapi.Response(
                description="Term and Condition partially updated successfully", 
                schema=StandardResponseSchema
            ),
            400: openapi.Response(
                description="Validation failed"
            ),
            404: openapi.Response(
                description="Term and Condition not found"
            ),
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Term and Condition ID", type=openapi.TYPE_INTEGER)]
    )
    def patch(self, *args, **kwargs):
        try:
            instance = TermsAndConditionmodel.objects.get(pk=kwargs['pk'])
        except TermsAndConditionmodel.DoesNotExist:
            raise NotFound("Term and Condition not found")
        
        serializer = self.serializer_class(instance, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Term and Condition Partially Updated Successfully",
                "data": serializer.data  
            })
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors  
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a Term and Condition",
        responses={
            204: openapi.Response(
                description="Term and Condition deleted successfully", 
                schema=StandardResponseSchema
            ),
            404: openapi.Response(
                description="Term and Condition not found"
            ),
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Term and Condition ID", type=openapi.TYPE_INTEGER)]
    )
    def delete(self, *args, **kwargs):
        try:
            instance = TermsAndConditionmodel.objects.get(pk=kwargs['pk'])
        except TermsAndConditionmodel.DoesNotExist:
            raise NotFound("Term and Condition not found")
        
        instance.delete()
        return Response({
            "status": 204,
            "message": "Term and Condition Deleted Successfully",
            "data": {}  
        }, status=status.HTTP_204_NO_CONTENT)



class PrivacyPolicyView(APIView):
    serializer_class = TermsAndConditionSerializer  

    StandardResponseSchema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    )

    @swagger_auto_schema(
        operation_description="Retrieve a list or a specific Privacy Policy by ID",
        responses={
            200: openapi.Response('Privacy Policy retrieved successfully', TermsAndConditionSerializer(many=True)),
            404: openapi.Response('Privacy Policy not found')
        },
    )
    def get(self, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                instance = PrivacyPolicyModel.objects.get(pk=kwargs['pk'])
            except PrivacyPolicyModel.DoesNotExist:
                raise NotFound("Privacy policy not found")
            serializer = self.serializer_class(instance)
            return Response({
                "status": 200,
                "message": "Data Retrieved Successfully",
                "data": serializer.data
            })
        
        policy_model_obj = self.get_queryset()
        serializer = self.serializer_class(policy_model_obj, many=True)
        return Response({
            "status": 200,
            "message": "Data Retrieved Successfully",
            "data": serializer.data
        })

    def get_queryset(self):
        return PrivacyPolicyModel.objects.all()

    @swagger_auto_schema(
        operation_description="Create a new Privacy Policy",
        request_body=TermsAndConditionSerializer,  
        responses={
            201: openapi.Response('Privacy Policy created successfully', TermsAndConditionSerializer),
            400: openapi.Response('Validation failed')
        }
    )
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 201,
                "message": "Privacy Policy Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing Privacy Policy",
        request_body=TermsAndConditionSerializer,  
        responses={
            200: openapi.Response('Privacy Policy updated successfully', TermsAndConditionSerializer),
            400: openapi.Response('Validation failed'),
            404: openapi.Response('Privacy Policy not found')
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Privacy Policy ID", type=openapi.TYPE_INTEGER)]
    )
    def put(self, *args, **kwargs):
        try:
            instance = PrivacyPolicyModel.objects.get(pk=kwargs['pk'])
        except PrivacyPolicyModel.DoesNotExist:
            raise NotFound("Privacy policy not found")
        
        serializer = self.serializer_class(instance, data=self.request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Privacy Policy Updated Successfully",
                "data": serializer.data
            })
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update an existing Privacy Policy",
        request_body=TermsAndConditionSerializer, 
        responses={
            200: openapi.Response('Privacy Policy partially updated successfully', TermsAndConditionSerializer),
            400: openapi.Response('Validation failed'),
            404: openapi.Response('Privacy Policy not found')
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Privacy Policy ID", type=openapi.TYPE_INTEGER)]
    )
    def patch(self, *args, **kwargs):
        try:
            instance = PrivacyPolicyModel.objects.get(pk=kwargs['pk'])
        except PrivacyPolicyModel.DoesNotExist:
            raise NotFound("Privacy policy not found")
        
        serializer = self.serializer_class(instance, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Privacy Policy Partially Updated Successfully",
                "data": serializer.data
            })
        
        return Response({
            "status": 400,
            "message": "Validation Failed",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a Privacy Policy",
        responses={
            204: openapi.Response('Privacy Policy deleted successfully'),
            404: openapi.Response('Privacy Policy not found')
        },
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="Privacy Policy ID", type=openapi.TYPE_INTEGER)]
    )
    def delete(self, *args, **kwargs):
        try:
            instance = PrivacyPolicyModel.objects.get(pk=kwargs['pk'])
        except PrivacyPolicyModel.DoesNotExist:
            raise NotFound("Privacy policy not found")
        
        instance.delete()
        return Response({
            "status": 204,
            "message": "Privacy Policy Deleted Successfully"
        }, status=status.HTTP_204_NO_CONTENT)



class PricingPlanQueryView(generics.ListCreateAPIView):
    queryset = PricingPlanQueryModel.objects.all()
    serializer_class = PricingPlanQuerySerializer

    StandardResponseSchema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    )

    @swagger_auto_schema(
        operation_description="Retrieve the list of pricing plans",
        responses={
            200: openapi.Response(
                'List of pricing plans',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 200,
                        "message": "List of pricing plans retrieved successfully",
                        "data": []
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Submit a new pricing plan query",
        responses={
            201: openapi.Response(
                'Pricing plan query submitted successfully',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 201,
                        "message": "Pricing Plan Query Submitted Successfully",
                        "data": {}
                    }
                }
            ),
            400: openapi.Response(
                'Bad request',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 400,
                        "message": "Validation failed",
                        "data": {}
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 201, 
                "message": "Pricing Plan Query Submitted Successfully", 
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400, 
            'message': 'Validation Failed', 
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class ContactUsView(generics.ListCreateAPIView):
    queryset = ContactUsModel.objects.all()
    serializer_class = ContactUsSerializer

    StandardResponseSchema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    )

    @swagger_auto_schema(
        operation_description="Retrieve the list of contact form submissions",
        responses={
            200: openapi.Response(
                'List of contact form submissions',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 200,
                        "message": "List of contact forms retrieved successfully",
                        "data": []
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Submit a contact form",
        responses={
            201: openapi.Response(
                'Form submitted successfully',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 201,
                        "message": "Form Submitted Successfully",
                        "data": {}
                    }
                }
            ),
            400: openapi.Response(
                'Bad request',
                StandardResponseSchema,
                examples={
                    "application/json": {
                        "status": 400,
                        "message": "Validation failed",
                        "data": {}
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 201,
                'message': 'Form Submitted Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400,
            'message': 'Validation Failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class HiringView(generics.ListAPIView):
    serializer_class = HiringSerializer
    queryset = HiringModel.objects.all()

    StandardResponseSchema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
        }
    )

    @swagger_auto_schema(
        operation_description="Retrieve a list of hiring entries or a specific one by ID",
        responses={
            200: openapi.Response('Hiring retrieved successfully', HiringSerializer(many=True)),
            404: openapi.Response('Hiring not found')
        }
    )
    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                hiring_instance = HiringModel.objects.get(pk=pk)
                serializer = self.get_serializer(hiring_instance)
                return Response({
                    "status": 200,
                    "message": "Data retrieved successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except HiringModel.DoesNotExist:
                return Response({
                    "status": 404,
                    "message": "Hiring not found"
                }, status=status.HTTP_404_NOT_FOUND)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": 200,
            "message": "Data retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# class TenantObjectAttributeCreateView(generics.ListCreateAPIView):
#     def post(self, request, *args, **kwargs):
#         name = request.POST.get("name")
#         datatype = request.POST.get("datatype")
#         is_deleted = request.POST.get("is_deleted")
        
#         if name == name and datatype == datatype and is_deleted == is_deleted:
            
        








