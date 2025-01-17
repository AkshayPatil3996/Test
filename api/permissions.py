from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from opulatenant.models import *
from django.contrib.auth.models import GroupManager



def assign_permissions_to_groups():
    
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    tenant_group, _ = Group.objects.get_or_create(name="Tenant")
    tenant_employee_group, _ = Group.objects.get_or_create(name="TenantEmployee")

    # Admin group
    all_permissions = Permission.objects.all()
    admin_group.permissions.set(all_permissions)

    # Tenant group 
    tenant_permissions = [
        Permission.objects.get(content_type=ContentType.objects.get_for_model(TenantProfileModel), codename="view_tenant"),
        Permission.objects.get(content_type=ContentType.objects.get_for_model(TenantEmpModel), codename="view_tenant"),
    ]
    tenant_group.permissions.set(tenant_permissions)

    # TenantEmployee group 
    tenant_employee_permissions = [
        Permission.objects.get(content_type=ContentType.objects.get_for_model(TenantEmployeePermissionsModel), codename="view_employee_data"),
    ]
    tenant_employee_group.permissions.set(tenant_employee_permissions)











