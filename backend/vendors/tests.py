from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor

class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'test@example.com',
            'address': '123 Test Street',
            'vendor_code': 'VENDOR001'
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_get_vendor_list(self):
        url = reverse('vendor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor_data['name'])

    def test_get_vendor_detail(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-detail', args=[self.vendor.id])
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
        url = reverse('vendor-detail', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)