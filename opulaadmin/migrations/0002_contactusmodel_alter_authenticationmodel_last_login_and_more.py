# Generated by Django 4.2.16 on 2024-12-23 11:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opulaadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cum_first_name', models.CharField(max_length=50)),
                ('cum_last_name', models.CharField(max_length=50)),
                ('cum_email', models.EmailField(max_length=254)),
                ('cum_mobile_no', models.CharField(help_text='Enter mobile number', max_length=16, validators=[django.core.validators.RegexValidator(message='Mobile number must be 10 digits', regex='^\\+?\\d{1,4}?\\s?\\d{10}$')])),
                ('cum_subject', models.CharField(choices=[('GENERAL', 'General'), ('JOB', 'Job'), ('PARTNER', 'Partner')], max_length=50)),
                ('cum_message', models.TextField()),
                ('cum_created_at', models.DateTimeField(auto_now_add=True)),
                ('cum_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'admin_management"."contactus_management',
                'managed': True,
            },
        ),
        migrations.AlterField(
            model_name='authenticationmodel',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='countrymastermodel',
            name='cm_country_code',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='tenantmodel',
            name='tm_auth',
            field=models.ForeignKey(db_column='tm_auth', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PricingPlanQueryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ppqm_first_name', models.CharField(max_length=50)),
                ('ppqm_last_name', models.CharField(max_length=50)),
                ('ppqm_email', models.EmailField(max_length=254)),
                ('ppqm_company_name', models.CharField(max_length=100)),
                ('ppqm_mobile_no', models.CharField(help_text='Enter mobile number', max_length=16, validators=[django.core.validators.RegexValidator(message='Mobile number must be 10 digits', regex='^\\+?\\d{1,4}?\\s?\\d{10}$')])),
                ('ppqm_type', models.CharField(choices=[('B2B', 'B2B'), ('B2C', 'B2C'), ('BOTH', 'Both')], max_length=30)),
                ('ppqm_created_at', models.DateTimeField(auto_now_add=True)),
                ('ppqm_updated_at', models.DateTimeField(auto_now=True)),
                ('ppqm_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opulaadmin.countrymastermodel')),
                ('ppqm_industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opulaadmin.industrymastermodel')),
            ],
            options={
                'db_table': 'admin_management"."pricing_plan_query_management',
                'managed': True,
            },
        ),
    ]