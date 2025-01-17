from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from opulaadmin.models import *
import uuid

   
class TenantProfileModel(models.Model):
    pan_number_validator = RegexValidator(
    regex=r'^[A-Z]{5}[0-9]{4}[A-Z]$', 
    message="Enter a valid PAN number (format: AAAAA9999A)"
)
    gst_validator = RegexValidator(
    regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[A-Z]{1}[0-9]{1}$',
    message="Enter a valid GST number (format: XXAAAAA1234A1Z1)",
) 
    tpm_tenant_user = models.ForeignKey(AuthenticationModel, on_delete=models.CASCADE, db_column='tpm_tenant_user')
    tpm_organization = models.CharField(max_length=52)
    tpm_industry = models.ForeignKey(IndustryMasterModel, on_delete=models.CASCADE, db_column='tpm_industry')
    tpm_pan_no = models.CharField(
        max_length=10, 
        validators=[pan_number_validator], 
        unique=True,  
        help_text="Enter a valid PAN number (format: AAAAA9999A)"
    )
    tpm_gst_no = models.CharField(
        max_length=15,
        validators=[gst_validator],
        help_text="Enter a valid GST number (format, 27AACCG1234F1Z5)"
    )
    tpm_created_at = models.DateTimeField(auto_now_add=True)
    tpm_upadated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'management"."tenantprofilemanagement' 
        managed = True

class TenantEmpModel(models.Model):
    tem_tenant = models.ForeignKey(TenantModel, on_delete=models.CASCADE, db_column='tem_tenant')
    tem_tenant_emp = models.ForeignKey(AuthenticationModel, on_delete=models.CASCADE, db_column='tem_tenant_emp')

    class Meta:
        db_table = 'employee_management"."tenantemployeemanagement' 
        managed = True







    




