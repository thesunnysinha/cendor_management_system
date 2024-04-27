from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(),name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
]