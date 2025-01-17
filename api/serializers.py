from rest_framework import serializers


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from opulaadmin.models import *

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff  

@user_passes_test(is_admin)
def some_admin_view(request):
    pass

class StandardResponseSchema(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.JSONField()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleManagementModel
        fields = '__all__'


class AuthenticationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Password fields didn't match."})
        return data

    def validate_email(self, value):
        if AuthenticationModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    class Meta:
        model = AuthenticationModel
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'am_mobile_no']

    def create(self, validated_data):
        static_role = RoleManagementModel.objects.get(id=2)
        user = AuthenticationModel.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            am_mobile_no=validated_data['am_mobile_no'],
            am_role=static_role
        )

        return user
    


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantModel
        fields = '__all__'

    def validate_tm_auth(self, value):
        if not value:
            raise serializers.ValidationError("tm_auth cannot be null.")
        return value

    
class TermsAndConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditionmodel
        fields = "__all__"

class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicyModel
        field = "__all__"

class JobSkillModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkillModel
        field = "__all__"

class HiringSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringModel
        fields = "__all__"

class PricingPlanQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlanQueryModel
        fields = [
            'ppqm_first_name','ppqm_last_name','ppqm_email','ppqm_company_name',
            'ppqm_mobile_no','ppqm_country','ppqm_type','ppqm_industry'
            ]

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = [
            'cum_first_name','cum_last_name','cum_email', 'cum_mobile_no',
            'cum_subject', 'cum_message'
            ]




