from django.contrib import admin
from django.urls import path,include
from api import urls as api_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

#generating the api schema for swagger-ui or redoc
schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management System API",
      default_version='v1',
      description="Vendor Management System APIs Documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
]


################## IN DEBUG MODE SHOW ADMIN ##################
if settings.DEBUG:
   urlpatterns += [
      path('admin/', admin.site.urls),
   ]



########### Api ####################
urlpatterns += [
    path('api/', include(api_urls)),
]

############### Swagger && Redoc ###################
urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]