from django.urls import path,include
from vendors import urls as vendors_urls
from purchaseOrders import urls as purchaseOrders_urls
from authApp import urls as authApp_urls

urlpatterns = [
    ############ Vendors #################
    path("vendors/",include(vendors_urls)),
    ############ Purchase Orders #########
    path("purchase_orders/",include(purchaseOrders_urls)),
    ############ User ####################
    path("user/",include(authApp_urls)),
]