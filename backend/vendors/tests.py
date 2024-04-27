from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor
import uuid
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class VendorAPITests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user_data = {
            'email': 'test@example.com',
            'password': 'admin@123',
            'first_name': 'Test',
            'last_name': 'User',
            'username':'admin'
        }
        cls.user = User.objects.create_user(**cls.user_data)
        cls.refresh_token = RefreshToken.for_user(cls.user)
        cls.access_token = cls.refresh_token.access_token
    
    def generate_vendor_payload(self):
        return {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test Street',
            'vendor_code': uuid.uuid4()
        }
        
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test Street',
            'vendor_code': uuid.uuid4()
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    # In your test case
    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        response = self.client.post(url, self.generate_vendor_payload(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_get_vendor_list(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor_data['name'])

    def test_get_vendor_detail(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        updated_data = {
            'name': 'Updated Vendor Name',
            'contact_details': 'updated_test@example.com',
            'address': '456 Updated Street',
            'vendor_code': 'VENDOR002'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure response data contains expected keys
        expected_keys = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        for key in expected_keys:
            self.assertIn(key, response.data)
