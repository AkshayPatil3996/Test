from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class AuthenticationModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = AuthenticationModel
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'am_mobile_no']
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password 


class AdminLoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=70, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    class Meta:
        model = AuthenticationModel  
        fields = ['email', 'password']

class TenantModelForm(forms.ModelForm):
    class Meta:
        model = TenantModel
        fields = ['tm_auth', 'tm_db_name', 'tm_db_user', 'tm_db_password', 'tm_domain_name']

    def save(self, commit=True):
        tenant = super().save(commit=False)
        if commit:
            tenant.save()
        return tenant
    
class TermsAndConditionForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditionmodel
        fields = ['tacm_title', 'tacm_content']

class PrivacyPolicyForm(forms.ModelForm):
    class Meta:
        model = PrivacyPolicyModel
        fields = ['ppm_title', 'ppm_content']

class JobSkillForm(forms.ModelForm):
    class Meta:
        model = JobSkillModel
        fields = ["jsm_skill"]

class IndustryForm(forms.ModelForm):
    class Meta:
        model = IndustryMasterModel
        fields = ["im_industry"]

class HiringForm(forms.ModelForm):
    class Meta:
        model = HiringModel
        fields = "__all__"




