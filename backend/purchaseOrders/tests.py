from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import PurchaseOrder
from vendor.models import Vendor

class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test Street', vendor_code='VENDOR001')
        self.purchase_order_data = {
            'po_number': 'PO001',
            'vendor': self.vendor.id,
            'order_date': '2024-04-26T12:00:00Z',
            'delivery_date': '2024-05-01T12:00:00Z',
            'items': [{'name': 'Item 1', 'quantity': 10}],
            'quantity': 10,
            'status': 'pending'
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        response = self.client.post(url, self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_get_purchase_order_list(self):
        url = reverse('purchaseorder-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['po_number'], self.purchase_order_data['po_number'])

    def test_get_purchase_order_detail(self):
        url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], self.purchase_order_data['po_number'])

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
        updated_data = {
            'po_number': 'PO002',
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
        url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)

    def test_acknowledge_purchase_order(self):
        url = reverse('purchaseorder-acknowledge', args=[self.purchase_order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)

    def test_vendor_performance(self):
        url = reverse('vendor-performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure response data contains expected keys
        expected_keys = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        for key in expected_keys:
            self.assertIn(key, response.data)
