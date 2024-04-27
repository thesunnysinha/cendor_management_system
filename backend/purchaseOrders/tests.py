from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from vendors.models import Vendor
from .models import PurchaseOrder
import uuid
from django.contrib.auth.models import User

class PurchaseOrderAPITests(TestCase):
    
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

    def generate_purchase_orders(self):
        return {
            'po_number': str(uuid.uuid4()),
            'vendor': self.vendor.id,
            'delivery_date': '2024-05-01T12:00:00Z',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending',
        }
        
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.vendor_data = {
            'name': 'Test Vendor2',
            'contact_details': 'test2@example.com',
            'address': '123 Test Street',
            'vendor_code': str(uuid.uuid4())
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)
        
        self.uuid = str(uuid.uuid4())
        self.purchase_order_data = {
            'po_number': self.uuid,
            'vendor_id': self.vendor.id,
            'delivery_date': '2024-05-01T12:00:00Z',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending',
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        url = reverse('purchase-order-list-create')
        response = self.client.post(url, self.generate_purchase_orders(), format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_get_purchase_order_list(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['po_number'], self.purchase_order_data['po_number'])

    def test_get_purchase_order_detail(self):
        url = reverse('purchase-order-retrieve-update-destroy', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order_data['po_number'])

    def test_update_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', args=[self.purchase_order.id])
        updated_data = {
            'po_number': self.uuid,
            'vendor': self.vendor.id,
            'order_date': '2024-04-26T12:00:00Z',
            'delivery_date': '2024-05-01T12:00:00Z',
            'items': [{'name': 'Updated Item 1', 'quantity': 20}],
            'quantity': 20,
            'status': 'completed'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, updated_data['po_number'])

    def test_delete_purchase_order(self):
        url = reverse('purchase-order-retrieve-update-destroy', args=[self.purchase_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        url = reverse('purchase-order-acknowledge', args=[self.purchase_order.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)
