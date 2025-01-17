from django.urls import path
from.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Tenant Management API",
      default_version='v1',
      description="API documentation for tenant and authentication management",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@tenantmanagement.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    

    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    path('api/v1/terms/and/condition', TermsAndConditionView.as_view(), name='terms_and_condition'),
    path('api/v1/terms/and/condition/<int:pk>', TermsAndConditionView.as_view(), name='terms_and_condition'),

    path('api/v1/privacy/policy', PrivacyPolicyView.as_view(), name='terms_and_condition'),
    path('api/v1/privacy/policy/<int:pk>', PrivacyPolicyView.as_view(), name='terms_and_condition'),

    path('api/v1/role', RoleView.as_view(), name='role'),
    path("api/v1/register", TenantRegistrationView.as_view(), name='register'),
    path('api/v1/login', TenantLoginView.as_view(), name='login'),


    path('api/v1/auth/list/<str:role>', TenantAuthView.as_view(), name='get_tanant'),

# WEBSITE API
   path('api/v1/pricing/plan/form', PricingPlanQueryView.as_view(), name='pricing_plan'),
   path("api/v1/contact/form", ContactUsView.as_view(), name='contact_us'),
   path("api/v1/hiring", HiringView.as_view(), name='hiring'),
   path("api/v1/hiring/<int:pk>", HiringView.as_view(), name='hiring')


]
 
 