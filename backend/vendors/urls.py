from django.urls import path
from . import views

urlpatterns = [
    path('', views.VendorListCreate.as_view(), name='vendor-list-create'),
    path('<int:pk>/', views.VendorRetrieveUpdateDestroy.as_view(), name='vendor-retrieve-update-destroy'),
    path('<int:pk>/performance/', views.VendorPerformance.as_view(), name='vendor-performance'),
]