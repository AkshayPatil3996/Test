from django.urls import path
from.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('privacy/policy', privacy_policy_view, name='privacy_policy'),
    path('terms/and/condition', terms_and_conditions_view, name='terms_and_condition'),

    # Test
    path("login/", admin_login_view, name='admin_login'),
    path("register/", admin_registration_view, name='admin_register'),
    path("staff/list", staff_list_view, name='staff_list'),
    # path("tenant/login", login_view, name='login'),
    path("dashboard", dashboard_view, name='dashboard'),
    path("tenant/list", tenant_list_and_update_view, name='tenant_list'),
    path("tenant/manage/<int:pk>", admin_tenant_manage_view, name='tenant_manage'),
    path("tenant/profile/<int:pk>", tenant_profile_view, name='tenant_profile'),
    path("tenant/employee/list", tenant_employee_list_view, name='tenant_employee_list'),
    path("tenant/employee/profile", tenant_employee_profile_view, name='tenant_employee_profile'),
    # path("create/staff/register", admin_tenant_manage_view, name='create_staff_register'),

    path("hiring/create/job", hiring_create_view, name="create_job"),
    path("hiring/job/list/", hiring_job_list_view, name="job_list"),
    path("miscellaneous", miscellaneous_view, name="miscellaneous"),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    # main
    # path("", home, name='home'),
    # path("dashboard", dashboard_view, name='dashboard'),
    # path("tenant/list", tenant_list_view, name='tenant_list'),
    # path("tenant/profile", tenant_profile_view, name='tenant_profile'),
    # path("tenant/employee/list", tenant_employee_list_view, name='tenant_employee_list'),
    # path("tenant/employee/profile", tenant_employee_profile_view, name='tenant_employee_profile'),
    # path("create/staff/register", create_staff_register_view, name='create_staff_register'),
  
]