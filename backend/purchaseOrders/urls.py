from django.urls import path
from . import views

urlpatterns = [
    path('', views.PurchaseOrderListCreate.as_view(), name='purchase-order-list-create'),
    path('<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase-order-retrieve-update-destroy'),
    path('<int:pk>/acknowledge/', views.PurchaseOrderAcknowledge.as_view(), name='purchase-order-acknowledge'),
]