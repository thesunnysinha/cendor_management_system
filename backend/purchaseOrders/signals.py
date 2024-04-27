from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from vendors.models import HistoricalPerformance, PurchaseOrder
from vendors.views import VendorPerformance

vendor_performance = VendorPerformance()

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_purchase_order_change(sender, instance, created, **kwargs):
    if created or instance.status != instance._state.original_state.get('status'):
        vendor = instance.vendor
        performance_data = vendor_performance.calculate_performance_metrics(vendor)
        update_or_create_historical_performance(vendor, performance_data)

@receiver(post_delete, sender=PurchaseOrder)
def update_performance_metrics_on_purchase_order_delete(sender, instance, **kwargs):
    vendor = instance.vendor
    performance_data = vendor_performance.calculate_performance_metrics(vendor)
    update_or_create_historical_performance(vendor, performance_data)

def update_or_create_historical_performance(vendor, performance_data):
    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        date=timezone.now(),
        defaults={
            'on_time_delivery_rate': performance_data['on_time_delivery_rate'],
            'quality_rating_avg': performance_data['quality_rating_avg'],
            'average_response_time': performance_data['average_response_time'],
            'fulfillment_rate': performance_data['fulfillment_rate']
        }
    )
