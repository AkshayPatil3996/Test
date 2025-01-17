from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
import uuid
import json


# Create your models here.

class CountryMasterModel(models.Model):
    cm_international_dial = models.CharField(max_length=15)
    cm_country_code = models.CharField(max_length=6)
    cm_country_name = models.CharField(max_length=50)  
    cm_created_at = models.DateTimeField(auto_now_add=True)
    cm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master"."countrymanagement' 
        managed = True



class IndustryMasterModel(models.Model):
    im_industry = models.CharField(max_length=30)
    im_created_at = models.DateTimeField(auto_now_add=True)
    im_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master"."industrymanagement' 
        managed = True


class PricingPlanQueryModel(models.Model):

    mobile_number_validator = RegexValidator(regex=r'^\+?\d{1,4}?\s?\d{10}$', message="Mobile number must be 10 digits")


    SELECT_TYPE = (
        ("B2B", "B2B"),
        ('B2C', "B2C"),
        ("BOTH", "Both"),
    )
    
    ppqm_first_name = models.CharField(max_length=50)
    ppqm_last_name = models.CharField(max_length=50)
    ppqm_email = models.EmailField()
    ppqm_company_name = models.CharField(max_length=100)
    ppqm_mobile_no = models.CharField(max_length=16, validators=[mobile_number_validator], help_text="Enter mobile number")
    ppqm_country = models.ForeignKey(CountryMasterModel, on_delete=models.CASCADE)
    ppqm_type = models.CharField(max_length=30, choices=SELECT_TYPE)
    ppqm_industry = models.ForeignKey(IndustryMasterModel, on_delete=models.CASCADE)
    ppqm_created_at = models.DateTimeField(auto_now_add=True)
    ppqm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_management"."pricing_plan_query_management'
        managed = True


class ContactUsModel(models.Model):

    SELECT_SUBJECT = (
        ("GENERAL", "General"),
        ('JOB', "Job"),
        ("PARTNER", "Partner"),
    )

    mobile_number_validator = RegexValidator(regex=r'^\+?\d{1,4}?\s?\d{10}$', message="Mobile number must be 10 digits")

    cum_first_name = models.CharField(max_length=50)
    cum_last_name = models.CharField(max_length=50)
    cum_email = models.EmailField()
    cum_mobile_no = models.CharField(max_length=16, validators=[mobile_number_validator], help_text="Enter mobile number")
    cum_subject = models.CharField(max_length=50, choices=SELECT_SUBJECT)
    cum_message = models.TextField()
    cum_created_at = models.DateTimeField(auto_now_add=True)
    cum_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_management"."contactus_management'
        managed = True




class RoleManagementModel(models.Model):
    rm_role = models.CharField(max_length=15)
    rm_created_at = models.DateTimeField(auto_now_add=True)
    rm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master"."rolemanagement' 
        managed = True

        # "rm_updated_at": self.rm_updated_at.strftime('%Y-%m-%d %H:%M:%S'),
          

class AuthManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

class AuthenticationModel(AbstractBaseUser, PermissionsMixin):
    mobile_number_validator = RegexValidator(regex=r'^\+?\d{1,4}?\s?\d{10}$', message="Mobile number must be 10 digits")

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    am_mobile_no = models.CharField(max_length=16, validators=[mobile_number_validator], help_text="Enter mobile number")
    am_role = models.ForeignKey(RoleManagementModel, on_delete=models.CASCADE, null=True)
    am_is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True, null=True)
    am_created_at = models.DateTimeField(auto_now_add=True)
    am_updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['am_role']  

    objects = AuthManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'admin_management"."authmanagement'
        managed = True

    

class TenantModel(models.Model):
    def validate_subdomain(value):
        SUBDOMAIN_REGEX = r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*$'
        IP_ADDRESS_REGEX = r'^(?!\d{1,3}\.)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
   
        if re.match(IP_ADDRESS_REGEX, value):
            raise ValidationError(_('Subdomain cannot be an IP address.'))

        if not re.match(SUBDOMAIN_REGEX, value):
            raise ValidationError(_('Invalid subdomain format. Only letters, numbers, and hyphens are allowed, and it cannot start or end with a hyphen.'))

        if len(value) > 30:
            raise ValidationError(_('Subdomain cannot be longer than 30 characters.'))
        return value

    tm_auth = models.ForeignKey(AuthenticationModel, on_delete=models.CASCADE, db_column='tm_auth')  
    tm_db_name = models.CharField(max_length=70, unique=True)
    tm_db_user = models.CharField(max_length=244)
    tm_db_password = models.CharField(max_length=256)
    tm_domain_name = models.CharField(max_length=30, null=True, validators=[validate_subdomain], unique=True)
    tm_created_at = models.DateTimeField(auto_now_add=True)
    tm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_management"."tenantmanagement'
        managed = True


class TermsAndConditionmodel(models.Model):
    tacm_title = models.CharField(max_length=100)
    tacm_content = models.TextField()
    tacm_created_at = models.DateTimeField(auto_now_add=True)
    tacm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_management"."termandconditionmanagement' 
        managed = True


class PrivacyPolicyModel(models.Model):
    ppm_title = models.CharField(max_length=100)
    ppm_content = models.TextField()
    ppm_created_at = models.DateTimeField(auto_now_add=True)
    ppm_updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'admin_management"."privacypolicymanagement' 
        managed = True


class JobSkillModel(models.Model):
    jsm_skill = models.CharField(max_length=30)
    jsm_created_at = models.DateTimeField(auto_now_add=True)
    jsm_updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = 'admin_management"."jobskillmanagement' 
        managed = True


class HiringModel(models.Model):
    hm_job_title = models.CharField(max_length=30)
    hm_job_description = models.TextField()
    hm_start_date = models.CharField(max_length=15)
    hm_experience = models.CharField(max_length=10)
    hm_salary = models.CharField(max_length=20)
    hm_job_skills = models.ManyToManyField(JobSkillModel, related_name='hiring_jobs')
    hm_qualification = models.TextField()
    hm_responsibility = models.TextField()
    hm_last_submission_date = models.CharField(max_length=15)
    hm_created_at = models.DateTimeField(auto_now_add=True)
    hm_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_management"."hiringmanagement' 
        managed = True




  
  
   






