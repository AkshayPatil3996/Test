from django.db import connection,connections, DatabaseError
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from opulatenant.models import *
from django.conf import *
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import User
from .permissions import *
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from .permissions import *
from django.contrib.auth.models import AnonymousUser
import psycopg2
from django.core.exceptions import ObjectDoesNotExist
from cryptography.fernet import Fernet
import threading
from django.urls import reverse
from django.http import HttpResponse
from .db_routers import *
from django.contrib.sessions.models import Session
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
import redis

# Set up logging

thread_local = threading.local()


# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def get_redis_client(self):
#         """Connect to Redis server."""
#         return redis.StrictRedis.from_url(settings.REDIS_URL)

#     def __call__(self, request):
#         """Main middleware processing logic."""
#         # Step 1: Check if the URL is public and does not require authentication
#         if self.is_public_url(request):
#             # Skip authentication if the URL is public
#             return self.get_response(request)

#         # Step 2: Extract subdomain (tenant identifier) from the request
#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]  # This should be the subdomain, e.g., 'anmol5'

#         # Step 3: Check if tokens are available in cookies (access and refresh tokens)
#         access_token = request.COOKIES.get('access_token')
#         refresh_token = request.COOKIES.get('refresh_token')

#         if access_token and refresh_token:
#             print("access_token-------", access_token)
#             user = self.authenticate_user_from_token(access_token)
#             if user:
#                 if self.is_user_associated_with_tenant(user, prefix):
#                     request.user = user
#                     return self.handle_tenant_db_setup(request)
#                 else:
#                     return HttpResponse("You are not authorized to access this tenant.", status=403)

#         # Step 4: If no tokens in cookies, check Redis for tokens
#         token = self.get_token_from_redis(request)
#         if token:
#             user = self.authenticate_user_from_token(token)
#             if user:
#                 if self.is_user_associated_with_tenant(user, prefix):
#                     request.user = user
#                     return self.handle_tenant_db_setup(request)
#                 else:
#                     return HttpResponse("You are not authorized to access this tenant.", status=403)

#         # Step 5: If no tokens found (cookies or Redis), check if user exists
#         user_id = request.COOKIES.get('user_id')  # Assuming you store user_id in cookies

#         if user_id:
#             try:
#                 user = get_user_model().objects.get(id=user_id)
#                 # If the user exists but no token found, redirect to login
#                 return redirect('login_url')  # Replace with your actual login URL

#             except get_user_model().DoesNotExist:
#                 pass

#         # Step 6: If no tokens and no user exists, deny access
#         return HttpResponse("You must be logged in to access this URL.", status=403)

#     def is_public_url(self, request):
#         """Check if the URL is public and does not require authentication."""
#         # List of public URLs or domains that don't need authentication
#         public_urls = ['/', '/login/', '/register/', '/health/', '/public/']

#         # Allow access if the requested URL is in the public URLs list
#         if request.path in public_urls:
#             return True

#         # You can also check for specific subdomains that are publicly accessible
#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]

#         # List of public subdomains
#         public_subdomains = ['localhost', '127', 'www', settings.PUBLIC_DOMAIN]

#         if prefix in public_subdomains:
#             return True

#         return False

#     def authenticate_user_from_token(self, token):
#         """Authenticate the user from the provided token."""
#         try:
#             # Decode the token to extract user info
#             access_token = AccessToken(token)
#             user_id = access_token['user_id']
#             print("userid----------", user_id)
#             user = get_user_model().objects.get(id=user_id)
#             return user
#         except (InvalidToken, TokenError, get_user_model().DoesNotExist) as e:
#             print(f"Token error: {e}")
#             return None

#     def is_user_associated_with_tenant(self, user, tenant_prefix):
#         """Check if the user is associated with the specified tenant (based on subdomain)."""
#         try:
#             # Check if the tenant with the given prefix exists and the user matches the tenant's assigned user
#             tenant = TenantModel.objects.using('default').get(tm_domain_name=tenant_prefix)
#             return tenant.tm_auth.id == user.id
#         except TenantModel.DoesNotExist:
#             return False

#     def handle_tenant_db_setup(self, request):
#         """Setup the tenant database connection if the user is authenticated."""
#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]  # Extract subdomain prefix

#         # Only allow access if the prefix is in the list of allowed subdomains
#         if prefix in ['localhost', '127', '59', settings.PUBLIC_DOMAIN]:
#             return self.get_response(request)

#         if not request.user.is_authenticated:
#             return HttpResponse("You must be logged in to access this URL.", status=403)

#         # Tenant database setup for the specific subdomain
#         if prefix:
#             try:
#                 tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix, tm_auth=request.user.id)

#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password

#                 # Decrypt the database password
#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 # Tenant database configuration
#                 tenant_db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                     'ENGINE': settings.DATABASES['default']['ENGINE'],
#                     'TIME_ZONE': settings.TIME_ZONE,
#                     'USE_TZ': settings.USE_TZ,
#                     'CONN_HEALTH_CHECKS': True,
#                     'CONN_MAX_AGE': None,
#                     'OPTIONS': {},
#                     'AUTOCOMMIT': True,
#                     'ATOMIC_REQUESTS': True,
#                 }

#                 alias = f"tenant_{prefix}"
#                 connections.databases[alias] = tenant_db_config

#                 # Set the search path for the tenant database (optional)
#                 with connections[alias].cursor() as cursor:
#                     cursor.execute("SET search_path TO management;")

#             except TenantModel.DoesNotExist:
#                 return HttpResponse("Tenant not found.", status=404)

#             except Exception as e:
#                 return HttpResponse(f"Unexpected error: {str(e)}", status=500)

#         return self.get_response(request)

#     def get_token_from_redis(self, request):
#         """Retrieve access and refresh tokens from Redis."""
#         redis_client = self.get_redis_client()

#         # Extract tenant prefix (subdomain) from the request host
#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]

#         # Try to find the tenant associated with the subdomain prefix
#         try:
#             tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix)
#         except TenantModel.DoesNotExist:
#             return None

#         # Construct Redis token keys based on tenant's associated user ID
#         access_token_key = f"user:{tenant.tm_auth.id}:access_token"
#         refresh_token_key = f"user:{tenant.tm_auth.id}:refresh_token"

#         access_token = redis_client.get(access_token_key)
#         refresh_token = redis_client.get(refresh_token_key)

#         print("access token", access_token)

#         # If both tokens are available and valid, return the access token
#         if access_token and refresh_token:
#             print("decoded token---", access_token.decode('utf-8'))
#             return access_token.decode('utf-8')

#         # If access token is expired, attempt to refresh using the refresh token
#         elif refresh_token:
#             return self.refresh_tokens(redis_client, request.user, refresh_token.decode('utf-8'))

#         return None

#     def refresh_tokens(self, redis_client, user, refresh_token):
#         """Handle refreshing tokens when access token is expired."""
#         try:
#             # Try to refresh the access token using the refresh token
#             refresh = RefreshToken(refresh_token)
#             if refresh:
#                 user_id = refresh['user_id']
#                 print('user_id12123-------', user_id)
#                 if user.id != user_id:
#                     return None  # Invalid user, return None.

#                 # Generate new access token
#                 new_access_token = str(refresh.access_token)
#                 new_refresh_token = str(refresh)

#                 # Update Redis with the new tokens
#                 redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, new_access_token)
#                 redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, new_refresh_token)

#                 return new_access_token

#             return None
#         except Exception as e:
#             print(f"Error refreshing tokens: {e}")
#             return None

class TenantMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def get_redis_client(self):
        return redis.StrictRedis.from_url(settings.REDIS_URL)

    def __call__(self, request):
        if self.is_public_url(request):
            return self.get_response(request)

        host = request.META.get('HTTP_HOST', '')
        domain = host.split(':')[0]
        prefix = domain.split('.')[0] 

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token and refresh_token:
            user = self.authenticate_user_from_token(access_token)
            if user:
                if self.is_user_associated_with_tenant(user, prefix):
                    request.user = user
                    return self.handle_tenant_db_setup(request)
                else:
                    return HttpResponse("You are not authorized to access this tenant.", status=403)

        token = self.get_token_from_redis(request)
        if token:
            user = self.authenticate_user_from_token(token)
            if user:
                if self.is_user_associated_with_tenant(user, prefix):
                    request.user = user
                    return self.handle_tenant_db_setup(request)
                else:
                    return HttpResponse("You are not authorized to access this tenant.", status=403)

        return HttpResponse("You must be logged in to access this URL.", status=403)

    def is_public_url(self, request):
        public_urls = ['/', '/login/', '/register/', '/health/', '/public/']

        if request.path in public_urls:
            return True

        host = request.META.get('HTTP_HOST', '')
        domain = host.split(':')[0]
        prefix = domain.split('.')[0]

        public_subdomains = ['localhost',"3", '59','127', 'www','13', settings.PUBLIC_DOMAIN]

        if prefix in public_subdomains:
            return True

        return False

    def authenticate_user_from_token(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = get_user_model().objects.get(id=user_id)
            return user
        except (InvalidToken, TokenError, get_user_model().DoesNotExist) as e:
            return None

    def is_user_associated_with_tenant(self, user, tenant_prefix):
        try:
            tenant = TenantModel.objects.using('default').get(tm_domain_name=tenant_prefix)
            return tenant.tm_auth.id == user.id
        except TenantModel.DoesNotExist:
            return False

    def handle_tenant_db_setup(self, request):
        host = request.META.get('HTTP_HOST', '')
        domain = host.split(':')[0]
        prefix = domain.split('.')[0] 

        if prefix in ['localhost', '127', '59', settings.PUBLIC_DOMAIN]:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to access this URL.", status=403)

        if prefix:
            try:
                tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix, tm_auth=request.user.id)

                tm_db_name = tenant.tm_db_name
                tm_db_user = tenant.tm_db_user
                tm_db_password = tenant.tm_db_password

                fernet = Fernet(settings.FERNET_KEY)
                decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

                tenant_db_config = {
                    'NAME': tm_db_name,
                    'USER': tm_db_user,
                    'PASSWORD': decrypted_password,
                    'HOST': settings.DATABASES['default']['HOST'],
                    'PORT': settings.DATABASES['default']['PORT'],
                    'ENGINE': settings.DATABASES['default']['ENGINE'],
                    'TIME_ZONE': settings.TIME_ZONE,
                    'USE_TZ': settings.USE_TZ,
                    'CONN_HEALTH_CHECKS': True,
                    'CONN_MAX_AGE': None,
                    'OPTIONS': {},
                    'AUTOCOMMIT': True,
                    'ATOMIC_REQUESTS': True,
                }

                alias = f"tenant_{prefix}"
                connections.databases[alias] = tenant_db_config

                with connections[alias].cursor() as cursor:
                    cursor.execute("SET search_path TO management;")

            except TenantModel.DoesNotExist:
                return HttpResponse("Tenant not found.", status=404)

            except Exception as e:
                return HttpResponse(f"Unexpected error: {str(e)}", status=500)

        return self.get_response(request)

    def get_token_from_redis(self, request):
        redis_client = self.get_redis_client()

        host = request.META.get('HTTP_HOST', '')
        domain = host.split(':')[0]
        prefix = domain.split('.')[0]

        try:
            tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix)
        except TenantModel.DoesNotExist:
            return None

        access_token_key = f"user:{tenant.tm_auth.id}:access_token"
        refresh_token_key = f"user:{tenant.tm_auth.id}:refresh_token"

        access_token = redis_client.get(access_token_key)
        refresh_token = redis_client.get(refresh_token_key)



        if access_token and refresh_token:
            return access_token.decode('utf-8')

        elif refresh_token:
            return self.refresh_tokens(redis_client, request.user, refresh_token.decode('utf-8'))

        return None

    def refresh_tokens(self, redis_client, user, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            if refresh:
                user_id = refresh['user_id']
                if user.id != user_id:
                    return None 

                new_access_token = str(refresh.access_token)
                new_refresh_token = str(refresh)

                redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, new_access_token)
                redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, new_refresh_token)

                return new_access_token

            return None
        except Exception as e:
            return None


# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def get_redis_client(self):
#         """Connect to Redis server."""
#         return redis.StrictRedis.from_url(settings.REDIS_URL)

#     def __call__(self, request):
       
#         with connections['default'].cursor() as cursor:
#             cursor.execute("SET search_path TO admin_management, public;")
  
#         # my_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1MjAzODM5LCJpYXQiOjE3MzUxOTcwNzQsImp0aSI6Ijc0MDA0YjY3ZmMxZTRhMWE5NTUzNGI0MzhmYWQ3MGM1IiwidXNlcl9pZCI6OX0.42MmzLue_qVWQeBdRyvXOXRl4i0WvvFw5oNtgRlZQKM"

      
#         # token = request.COOKIES.get('jwt_access_token') 
#         # print("token for access",token)
#         token = self.get_token_from_redis(request)
    
#         if token:
#             try:
               
#                 access_token = AccessToken(token)
    
#                 user_id = access_token['user_id']
#                 user = get_user_model().objects.get(id=user_id)
               
#                 request.user = user

#             except InvalidToken as e:
#                 print(f"Invalid token: {e}")
#                 request.user = None
#             except TokenError as e:
#                 print(f"Token error: {e}")
#                 request.user = None
#             except get_user_model().DoesNotExist:
#                 print(f"User with ID {user_id} not found.")
#                 request.user = None
#         else:
#             print("No JWT token found.")
#             request.user = None

#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0] 
#         prefix = domain.split('.')[0]  

#         if prefix in ['localhost', '127', '59', settings.PUBLIC_DOMAIN]:
#             with connections['default'].cursor() as cursor:
#                 cursor.execute("SET search_path TO admin_management, public;")
#             return self.get_response(request)
        
#         if not request.user or not request.user.is_authenticated:
#             return HttpResponse("You must be logged in to access this URL.", status=403)

#         if prefix:
#             try:
#                 tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix, tm_auth=user.id)
 
#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password

#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 tenant_db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                     'ENGINE': settings.DATABASES['default']['ENGINE'],
#                     'TIME_ZONE': settings.TIME_ZONE,
#                     'USE_TZ': settings.USE_TZ,
#                     'CONN_HEALTH_CHECKS': True,
#                     'CONN_MAX_AGE': None,
#                     'OPTIONS': {},
#                     'AUTOCOMMIT': True,
#                     'ATOMIC_REQUESTS': True,
#                 }

#                 alias = f"tenant_{prefix}"
#                 connections.databases[alias] = tenant_db_config

#                 with connections[alias].cursor() as cursor:
#                     cursor.execute("SET search_path TO management;")

#             except TenantModel.DoesNotExist:
#                 return HttpResponse("Tenant not found.", status=404)

#             except Exception as e:
#                 return HttpResponse(f"Unexpected error: {str(e)}", status=500)

#         response = self.get_response(request)
#         return response
    
#     def get_token_from_redis(self, request):
#         redis_client = self.get_redis_client()

#         tenant = TenantModel.objects.using('default').get(tm_domain_name=self.prefix)

#         access_token_key = f"user:{tenant.tm_auth}:access_token"
#         refresh_token_key = f"user:{tenant.tm_auth}:refresh_token"


#         access_token = redis_client.get(access_token_key)
#         refresh_token = redis_client.get(refresh_token_key)

#          # If both tokens are available and valid
#         if access_token and refresh_token:
#             return self.handle_valid_tokens(redis_client, user, access_token.decode('utf-8'), refresh_token.decode('utf-8'))

#         # If access token expired, attempt to refresh using the refresh token
#         elif refresh_token:
#             return self.refresh_tokens(redis_client, user, refresh_token.decode('utf-8'))

#         # If both tokens are expired or not found, generate new ones
#         else:
#             return self.generate_and_store_new_tokens(redis_client, user)
        
#     def handle_valid_tokens(self, redis_client, user, access_token, refresh_token):
#         """Handle the case when both access and refresh tokens are valid"""
#         return JsonResponse({
#             'message': 'Login successful',
#             'access_token': access_token,
#             'refresh_token': refresh_token
#         })

#     def refresh_tokens(self, redis_client, user, refresh_token):
#         """Handle refreshing tokens when access token is expired"""
#         try:
#             # Try to refresh the access token using the refresh token
#             refresh = RefreshToken(refresh_token)
#             if refresh:
#                 user_id = refresh['user_id']
#                 if user.id != user_id:
#                     return JsonResponse({'error': 'Invalid user'}, status=400)

#                 # Generate new access token
#                 new_access_token = str(refresh.access_token)
#                 new_refresh_token = str(refresh)
                
#                 redis_client = self.get_redis_client()

#                 # Update Redis with the new tokens
#                 redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, new_access_token)
#                 redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, new_refresh_token)

#                 return JsonResponse({
#                     "status": 200,
#                     'message': 'Tokens refreshed successfully',
#                     'access_token': new_access_token,
#                     'refresh_token': new_refresh_token
#                 })

#             return JsonResponse({'error': 'Invalid refresh token'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': 'Error refreshing tokens'}, status=500)

#     def generate_and_store_new_tokens(self, redis_client, user):
#         """Generate new access and refresh tokens if no valid tokens are found"""
#         try:
#             # Generate new refresh and access tokens
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)
            
#             redis_client = self.get_redis_client()

#             # Store the new tokens in Redis with expiration times
#             redis_client.setex(f"user:{user.id}:access_token", settings.JWT_TOKEN_LIFETIME, access_token)
#             redis_client.setex(f"user:{user.id}:refresh_token", settings.JWT_REFRESH_TOKEN_LIFETIME, refresh_token)

#             return JsonResponse({
#                 'message': 'Login successful',
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#             })

#         except Exception as e:
#             return JsonResponse({'error': 'Error generating tokens'}, status=500)
        
#     def get(self, request, *args, **kwargs):
#         """Handle the case where tokens are passed as cookies or via Redis"""
#         # Get the access and refresh tokens from Redis
#         redis_client = self.get_redis_client()
#         access_token = redis_client.get(f"user:{request.user.id}:access_token")
#         refresh_token = redis_client.get(f"user:{request.user.id}:refresh_token")

#         if access_token and refresh_token:
#             # Tokens found in Redis, check if the access token is valid
#             return self.refresh_tokens(request, access_token.decode('utf-8'), refresh_token.decode('utf-8'))

#         return JsonResponse({'error': 'No valid tokens found. Please log in again.'}, status=401)

    



        




class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        access_token = request.COOKIES.get('jwt_access_token')
        refresh_token = request.COOKIES.get('jwt_refresh_token')

      
        if access_token:
            try:
                AccessToken(access_token)  
                request.user = self.get_user_from_token(access_token)
            except TokenError:
               
                if refresh_token:
                    try:
                        refresh = RefreshToken(refresh_token)
                        new_access_token = str(refresh.access_token)

                        response = self.get_response(request)
                        response.set_cookie(
                            key='jwt_access_token',
                            value=new_access_token,
                            httponly=True,
                            secure=settings.SECURE_COOKIES, 
                            samesite='Strict',
                            max_age=settings.JWT_TOKEN_LIFETIME,
                        )

                        request.user = self.get_user_from_token(new_access_token)
                        return response
                    except TokenError:
                        return JsonResponse({"detail": "Token is expired or invalid. Please log in again."}, status=401)
                else:
                    return JsonResponse({"detail": "Token is expired or missing. Please log in again."}, status=401)
        elif refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)

                response = self.get_response(request)
                response.set_cookie(
                    key='jwt_access_token',
                    value=new_access_token,
                    httponly=True,
                    secure=settings.SECURE_COOKIES,  
                    samesite='Strict',
                    max_age=settings.JWT_TOKEN_LIFETIME,
                )

                request.user = self.get_user_from_token(new_access_token)
                return response
            except TokenError:
                return JsonResponse({"detail": "Token is expired or invalid. Please log in again."}, status=401)

        else:
            return self.generate_new_tokens(request)

    def generate_new_tokens(self, request):
        
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required."}, status=401)
        
        tokens = self.get_tokens_for_user(request.user)


        response = self.get_response(request)

        response.set_cookie(
            key='jwt_access_token',
            value=tokens['access_token'],
            httponly=True,
            secure=settings.SECURE_COOKIES,
            samesite='Strict',
            max_age=settings.JWT_TOKEN_LIFETIME,
        )

        response.set_cookie(
            key='jwt_refresh_token',
            value=tokens['refresh_token'],
            httponly=True,
            secure=settings.SECURE_COOKIES, 
            samesite='Strict',
            max_age=settings.JWT_REFRESH_TOKEN_LIFETIME,
        )

        return response

    def get_tokens_for_user(self, user):
        
        refresh = RefreshToken.for_user(user)

        refresh.payload['user_id'] = user.id  

        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def get_user_from_token(self, access_token):
       
        try:
            token = AccessToken(access_token)

            user_id = token['user_id']  
            user = AuthenticationModel.objects.get(id=user_id)  
            
            return user
        except (TokenError, AuthenticationModel.DoesNotExist):
            return None
 


# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
       

#         with connections['default'].cursor() as cursor:
#             cursor.execute("SET search_path TO admin_management, public;")

#         session_key = request.COOKIES.get('sessionid')
#         print("hshso",session_key)
        
#         if session_key:
#             try:
           
#                 session = Session.objects.using('default').get(pk=session_key)
#                 request.session = session.get_decoded()

#                 if request.user.is_authenticated:
#                     print(f"Authenticated user: {request.user}")
#                 else:
#                     print("User is not authenticated.")
#             except Session.DoesNotExist:
#                 print("Session does not exist.")
#                 request.user = None
#         else:
#             print("No session key found.")
#             request.user = None

#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]

#         if prefix in ['localhost', '127', '59', settings.PUBLIC_DOMAIN]:
#             with connections['default'].cursor() as cursor:
#                 cursor.execute("SET search_path TO admin_management, public;")
#             return self.get_response(request)

#         if prefix:
#             try:
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute("SET search_path TO admin_management, public;")
#                 # if not request.user or not request.user.is_authenticated:
#                 #     return HttpResponse("You must be logged in to access this URL.", status=403)
                

#                 tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix)
#                 print(f"Tenant found: {tenant.tm_domain_name}")

#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password
#                 print(f"Retrieved tenant DB credentials: db_name={tm_db_name}, db_user={tm_db_user}")

#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 tenant_db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                     'ENGINE': settings.DATABASES['default']['ENGINE'],
#                     'TIME_ZONE': settings.TIME_ZONE,
#                     'USE_TZ': settings.USE_TZ,
#                     'CONN_HEALTH_CHECKS': True,
#                     'CONN_MAX_AGE': None,
#                     'OPTIONS': {},
#                     'AUTOCOMMIT': True,
#                     'ATOMIC_REQUESTS': True,
#                 }

#                 alias = f"tenant_{prefix}"
#                 connections.databases[alias] = tenant_db_config
#                 print(f"Database alias '{alias}' added with configuration: {tenant_db_config}")

#                 with connections[alias].cursor() as cursor:
#                     cursor.execute("SET search_path TO management;")
#                 print(f"Connected to tenant's database and set search_path to management.")

#             except TenantModel.DoesNotExist:
#                 print(f"Tenant with domain '{prefix}' not found.")
#                 return HttpResponse("Tenant not found.", status=404)

#             except DatabaseError as e:
#                 print(f"Database connection error: {str(e)}")
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)

#             except Exception as e:
#                 print(f"Unexpected error: {str(e)}")
#                 return HttpResponse(f"Unexpected error: {str(e)}", status=500)

#         response = self.get_response(request)
#         return response



# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         User = get_user_model()
#         with connections['default'].cursor() as cursor:
#             cursor.execute("SET search_path TO admin_management, public;")
        

#         print("Session Key:", request.session.session_key)  # Check session key
#         print("Request User:", request.user)  # Debugging line to check user


#         # Debugging: Print the authenticated user
#         print("Request yhtruser:", request.user)  # Debugging line to check user
#         if request.user.is_authenticated:
#             print(f"Authenticated user: {request.user}")  # Debugging line to confirm authenticated user
#         else:
#             print("User is not authenticated.")  

#         host = request.META.get('HTTP_HOST', '')
#         domain = host.split(':')[0]
#         prefix = domain.split('.')[0]  
#         if prefix in ['localhost', '127', '59', settings.PUBLIC_DOMAIN]:
#             with connections['default'].cursor() as cursor:
#                 cursor.execute("SET search_path TO admin_management, public;")
#             return self.get_response(request)

#         if prefix:
#             try:
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute("SET search_path TO admin_management, public;")
#                 print("correct jfgjksn",request.session)
             
                
#                 # if not request.session:
#                 #     return HttpResponse("Your session not started yet", status=403)

#                 if not request.user.is_authenticated:
#                     return HttpResponse("You must be logged in to access this URL.", status=403)

#                 tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix)
#                 print(f"Tenant found: {tenant.tm_domain_name}")

#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password
#                 print(f"Retrieved tenant DB credentials: db_name={tm_db_name}, db_user={tm_db_user}")
              
#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 # Set up the tenant-specific database configuration
#                 tenant_db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                     'ENGINE': settings.DATABASES['default']['ENGINE'],
#                     'TIME_ZONE': settings.TIME_ZONE,
#                     'USE_TZ': settings.USE_TZ,
#                     'CONN_HEALTH_CHECKS': True,
#                     'CONN_MAX_AGE': 600,
#                     'OPTIONS': {},
#                     'AUTOCOMMIT': True,
#                     'ATOMIC_REQUESTS': True, 
#                 }

#                 # Dynamically create a database alias for this tenant
#                 alias = f"tenant_{prefix}"
#                 connections.databases[alias] = tenant_db_config
#                 print(f"Database alias '{alias}' added with configuration: {tenant_db_config}")

#                 # Set the search_path for this tenant database (to use the correct schema)
#                 with connections[alias].cursor() as cursor:
#                     cursor.execute("SET search_path TO management;")
#                 print(f"Connected to tenant's database and set search_path to management.")

#             except TenantModel.DoesNotExist:
#                 # Tenant not found for the given subdomain
#                 print(f"Tenant with domain '{prefix}' not found.")
#                 return HttpResponse("Tenant not found.", status=404)
#             except DatabaseError as e:
#                 # Handle database connection errors
#                 print(f"Database connection error: {str(e)}")
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)
#             except Exception as e:
#                 # Handle any other unexpected errors
#                 print(f"Unexpected error: {str(e)}")
#                 return HttpResponse(f"Unexpected error: {str(e)}", status=500)

#         # Proceed to the next middleware or view
#         response = self.get_response(request)
#         return response




# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         host = request.META.get('HTTP_HOST', '')
#         prefix = host.split('.')[0]

#         if host == settings.PUBLIC_DOMAIN or prefix in ['localhost', '59', "127"]:
#             with connections['default'].cursor() as cursor:
                   
#                 cursor.execute("SET search_path TO admin_management, public;")
#                 print("Connected to the default database and set search_path to admin_management.")

#             return self.get_response(request)

#         if prefix:
#             try:
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute("SET search_path TO admin_management, public;")
#                     print("Connected to the default database and set search_path to admin_management, public.")

#                 # if not request.user.is_authenticated():
#                 #     return HttpResponse("Must have authenticated to access this url", status=404)
                
#                 tenant = TenantModel.objects.using('default').get(tm_domain_name=prefix)
#                 print(f"Fetched tenant details: {tenant}")

#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password
#                 print(f"Retrieved tenant DB credentials: db_name={tm_db_name}, db_user={tm_db_user}")

#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 tenant_db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                     'ENGINE': settings.DATABASES['default']['ENGINE'],
#                     'TIME_ZONE': settings.TIME_ZONE,
#                     'USE_TZ': settings.USE_TZ,
#                     'CONN_HEALTH_CHECKS': True,
#                     'CONN_MAX_AGE': 600,
#                     'OPTIONS': {},
#                     'AUTOCOMMIT': True,
#                     'ATOMIC_REQUESTS': True, 
#                 }

#                 print("Tenant DB Config:", tenant_db_config)

#                 alias = f"tenant_{prefix}"
#                 connections.databases[alias] = tenant_db_config

#                 print(f"Database alias '{alias}' added with configuration: {tenant_db_config}")

#                 with connections[alias].cursor() as cursor:
#                     cursor.execute("SET search_path TO management;") 
#                     print("Connected to tenant's database and set search_path to management.")
#                 if not request.user.is_authenticated:
#                     return HttpResponse("Must be authenticated to access this URL.", status=404)

#             except TenantModel.DoesNotExist:
#                 print(f"Tenant with domain '{prefix}' not found.")
#                 return HttpResponse("Tenant not found.", status=404)
#             except DatabaseError as e:
#                 print(f"Database connection error: {str(e)}")
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)
#             except Exception as e:
#                 print(f"Unexpected error: {str(e)}")
#                 return HttpResponse(f"Unexpected error: {str(e)}", status=500)

#         # Proceed to the next middleware or view
#         response = self.get_response(request)
#         return response



# class TenantMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Get the subdomain from the request (e.g., tenant.localhost.com -> 'tenant')
#         host = request.get_host().split(':')[0]  # Get the host without port
#         subdomain = host.split('.')[0]  # Get the subdomain (e.g., 'tenant' from 'tenant.localhost.com')

#         # If the domain is public, do nothing and proceed with the normal response
#         if host == settings.PUBLIC_DOMAIN:
#             return self.get_response(request)

# #         # If localhost or 127, ensure to close and reconnect the default database
#         elif subdomain == 'localhost' or subdomain == '127':
#             connections['default'].connect()

#         try:
#             # Try to fetch the tenant from the database by subdomain
#             print("subdmainfdash--",subdomain)
#             tenant = TenantModel.objects.get(tm_domain_name=subdomain)

#             # Set tenant-specific database dynamically
#             self.set_tenant_database(tenant)

#             # Optionally, you can add the tenant object to the request to access later
#             request.tenant = tenant

#         except TenantModel.DoesNotExist:
#             # If tenant is not found, return a 404 response
#             return HttpResponse("Tenant not found", status=404)

#     def set_tenant_database(self, tenant):
#         # Dynamically set the tenant database connection settings
#         tenant_db_name = tenant.tm_db_name  # Each tenant has its own database

#         # You can create a connection dynamically if needed, but here we're assuming the tenant DB is already created
#         connections.databases['default'] = {
#             'ENGINE': 'django.db.backends.postgresql',  # Replace with the right DB engine
#             'NAME': tenant_db_name,
#             'USER': tenant.tm_db_user,
#             'PASSWORD': tenant.tm_db_password,
#             'HOST': 'localhost',
#             'PORT': '5432',
#         }

#         # Set this as the current database for tenant operations
#         connections['default'] = connections.databases['default'] = {
#             'ENGINE': 'django.db.backends.postgresql',  # Replace with the right DB engine
#             'NAME': tenant_db_name,
#             'USER': tenant.tm_db_user,
#             'PASSWORD': tenant.tm_db_password,
#             'HOST': 'localhost',
#             'PORT': '5432',
#         }




# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         host = request.META.get('HTTP_HOST', '')
#         prefix = host.split('.')[0]

#         # If the domain is public, do nothing and proceed with the normal response
#         if host == settings.PUBLIC_DOMAIN:
#             return self.get_response(request)

#         # If localhost or 127, ensure to close and reconnect the default database
#         elif prefix == 'localhost' or prefix == '127':
#             connections['default'].connect()

#         # If there's a prefix (tenant subdomain), attempt to resolve the tenant
#         elif prefix:
#             try:
#                 # If user is authenticated, resolve the tenant and switch schema
#                 # if request.user.is_authenticated:

#                 #     if request.user.is_authenticated:
#                 #         print("User is authenticated.")
#                 #     else:
#                 #         print("User is NOT authenticated.")
#                     # Try to find the tenant by the prefix
#                 # user_auth = AuthenticationModel.objects.get(email=request.user)
#                 tenant = TenantModel.objects.get(tm_domain_name=prefix)
                

#                 # Extract tenant database credentials
#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password

#                 # Decrypt the password using Fernet
#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 # Store tenant database connection details in thread-local storage
#                 thread_local.db_config = {
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                 }

#                 # Update the database connection settings with tenant-specific details
#                 connections['default'].close()
#                 connections['default'].settings_dict.update(thread_local.db_config)
#                 connections['default'].connect()

#                 # Set the schema dynamically for tenant (e.g., switch to the tenant's schema)
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute(f"SET search_path TO admin_management")

#                 # else:
#                 #     return HttpResponse("Unauthorized", status=401)

#             except TenantModel.DoesNotExist:
#                 return HttpResponse("Tenant not found.", status=404)
#             except DatabaseError as e:
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)

#         response = self.get_response(request)
#         return response


# class TenantMiddleware(MiddlewareMixin):
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         host = request.META.get('HTTP_HOST', '')
#         prefix = host.split('.')[0]

#         # If the domain is public, do nothing and proceed with the normal response
#         if host == settings.PUBLIC_DOMAIN:
#             return self.get_response(request)

#         # If localhost or 127, ensure to close and reconnect the default database
#         elif prefix == 'localhost' or prefix == '127':
#             connections['default'].connect()

#         # If there's a prefix, attempt to resolve the tenant
#         elif prefix:
#             try:
#                 # Try to find the tenant by the prefix
#                 tenant = TenantModel.objects.get(tm_domain_name=prefix)

#                 # Extract tenant database credentials
#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password

#                 # Decrypt the password using Fernet
#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 # Update the database connection settings with tenant-specific details
#                 connections['default'].close()
#                 connections['default'].settings_dict.update({
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                 })
#                 connections['default'].connect()

#                 # If schema switch is needed (ensure it's correct)
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute("SET search_path TO admin_management,public, master;")

#                 # You can now safely query tables in the 'admin_management' schema
#                 # Example: fetch tenant info if needed
#                 with connections['default'].cursor() as cursor:
#                     cursor.execute("SELECT * FROM admin_management.tenantmanagement LIMIT 1;")
#                     tenant_info = cursor.fetchone()
#                     print(tenant_info)

#             except TenantModel.DoesNotExist:
#                 return HttpResponse("Tenant not found.", status=404)
#             except DatabaseError as e:
#                 # Handle database connection error
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)
#             except ValidationError as e:
#                 return HttpResponse(f"Invalid tenant configuration: {str(e)}", status=400)

#         # If everything goes well, proceed with the normal response
#         response = self.get_response(request)
#         return response


#correct middleware
# class TenantMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         host = request.META.get('HTTP_HOST', '')  
#         prefix = host.split('.')[0] 

#         if prefix == 'localhost' or prefix == '127':
#             connections['default'].close() 
#             connections['default'].connect() 

#         elif prefix:
#             try:
#                 tenant = TenantModel.objects.get(tm_domain_name=prefix)

#                 tm_db_name = tenant.tm_db_name
#                 tm_db_user = tenant.tm_db_user
#                 tm_db_password = tenant.tm_db_password

#                 fernet = Fernet(settings.FERNET_KEY)
#                 decrypted_password = fernet.decrypt(tm_db_password.encode()).decode()

#                 connections['default'].close() 
#                 connections['default'].settings_dict.update({
#                     'NAME': tm_db_name,
#                     'USER': tm_db_user,
#                     'PASSWORD': decrypted_password,
#                     'HOST': settings.DATABASES['default']['HOST'],
#                     'PORT': settings.DATABASES['default']['PORT'],
#                 })

#                 connections['default'].connect()

#             except TenantModel.DoesNotExist:
#                 return HttpResponse("Tenant not found.", status=404)
#             except DatabaseError as e:
#                 return HttpResponse(f"Database connection error: {str(e)}", status=500)

#         response = self.get_response(request)
#         return response


# class TenantDatabaseMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         try:
#             public_url = settings.PUBLIC_URL
#         except AttributeError:
#             public_url = 'http://localhost:8000'  # Default to localhost if not set

#         # Extract the base domain name (without the port)
#         domain_name = request.get_host().split(":")[0]

#         # If the user is not authenticated (AnonymousUser), allow access to the public URL
#         # if isinstance(request.user, AnonymousUser):
#         #     # If the domain is the public URL domain, allow access
#         #     if domain_name == public_url.split("//")[1].split("/")[0]:
#         #         return None  # Don't redirect, just continue processing

#         #     # Redirect to the public URL if the domain is not the public domain
#         #     return HttpResponseRedirect(public_url)

#         # If the user is a superadmin, skip tenant-specific checks
#         if request.user.is_authenticated and hasattr(request.user, 'is_superuser') and request.user.is_superuser:
#             # Superadmin does not need to check for a tenant or domain; they can access the app without domain restriction
#             return None  # Let the request pass through without any database switching

#         # Look for the tenant associated with the domain
#         tenant = TenantModel.objects.filter(tm_domain_name=domain_name).first()

#         # If no tenant is found, redirect to the public URL
#         if not tenant:
#             return HttpResponseRedirect(public_url)
 
#         # Set the database name dynamically for the current request (tenant-specific DB)
#         connections['default'].settings_dict['NAME'] = tenant.tm_db_name

#     def process_response(self, request, response):
#         # Close the database connection after the request is processed
#         connections['default'].close()
#         return response


class RolesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.check_role_permissions(request)
        if not response:
            response = self.get_response(request)
        return response

    def check_role_permissions(self, request):
        user = request.user
        if user.is_authenticated:
            role = getattr(user, 'am_role', None) 

            if not role:
                return redirect(settings.LOGIN_URL)  

            role_name = role.rm_role  

            if role_name == "Admin":
                return None  

            if role_name == "Tenant":
                tenant_domain = request.get_host().split(":")[0]
                tenant = TenantModel.objects.filter(domain_name=tenant_domain).first()
                if tenant and tenant.tpm_tenant_user == user:
                    return None  
                else:
                    return redirect(settings.PUBLIC_URL)  

            if role_name == "TenantEmployee":
                tenant_employee = TenantEmpModel.objects.filter(tem_tenant_emp=user).first()
                if tenant_employee:
                    return None  
                else:
                    return redirect(settings.PUBLIC_URL) 

        return redirect(settings.LOGIN_URL)
        



