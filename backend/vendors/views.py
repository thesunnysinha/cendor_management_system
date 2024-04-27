from django.utils import timezone
from rest_framework import generics
from django.db.models import F, ExpressionWrapper, fields,Avg
from purchaseOrders.models import PurchaseOrder
from .models import Vendor
from .serializers import VendorSerializer, VendorPerformanceSerializer
from rest_framework.response import Response

class VendorListCreate(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorPerformance(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        performance_data = self.calculate_performance_metrics(vendor)
        serializer = self.get_serializer(performance_data)
        return Response(serializer.data)

    def calculate_performance_metrics(self, vendor):
        # On-Time Delivery Rate
        total_completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        on_time_deliveries = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        
        # Quality Rating Average
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

        # Average Response Time
        response_time_expr = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
        avg_response_time = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).annotate(response_time=response_time_expr).aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0

        # Fulfilment Rate
        total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        fulfillment_rate = (fulfilled_pos / total_pos) * 100 if total_pos > 0 else 0

        return {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time,
            'fulfillment_rate': fulfillment_rate
        }