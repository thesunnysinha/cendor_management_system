from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from vendors.views import VendorPerformance
from vendors.models import HistoricalPerformance
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class PurchaseOrderListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderAcknowledge(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Trigger the recalculation of average_response_time
        vendor = instance.vendor
        performance_data = VendorPerformance().calculate_performance_metrics(vendor)

        # Convert timedelta to total seconds
        average_response_time_seconds = performance_data['average_response_time'].total_seconds()

        # Update or create historical performance record
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={
                'on_time_delivery_rate': performance_data['on_time_delivery_rate'],
                'quality_rating_avg': performance_data['quality_rating_avg'],
                'average_response_time': average_response_time_seconds,  # Convert timedelta to total seconds
                'fulfillment_rate': performance_data['fulfillment_rate']
            }
        )

        return Response(self.get_serializer(instance).data)