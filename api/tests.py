from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
import uuid
from opulaadmin.models import *
from django.db import connection,connections

class TenantRegistrationViewTests(APITestCase):

    def test_valid_user_and_tenant_creation(self):

        with connections['default'].cursor() as cursor:
            cursor.execute("SET search_path TO admin_management, public, master;")

        user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'confirm_password': 'password123',
            'am_mobile_no': '1234567890',
            'tm_domain_name': 'example',
        }

        response = self.client.post('api/v1/register', user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User and Tenant created successfully')

        user = AuthenticationModel.objects.get(email='testuser@example.com')
        self.assertIsNotNone(user)


        tenant = TenantModel.objects.filter(tm_auth=user.id).first()  
        self.assertIsNotNone(tenant)
        self.assertEqual(tenant.tm_domain_name, 'example.com')


