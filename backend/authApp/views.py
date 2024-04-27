from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UserLoginSerializer,UserSignUpSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status,generics
from django.contrib.auth.models import User
from rest_framework.permissions import  AllowAny

#generate the token manually(both- access and refresh tokens)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#re-generate the access token by taking the refresh token
def refresh_tokens(refresh_token):
    try:
        refresh = RefreshToken(refresh_token)

        return {
            'access': str(refresh.access_token),
        }
    except Exception as e:
        return {"errors": {"token_error": str(e)}}
    
class UserLoginView(APIView):

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            user_token = get_tokens_for_user(user) 
            user_data = {
                "username": f"{username}",
                "first_name": f"{user.first_name}",
                "last_name": f"{user.last_name}",
                "email": f"{user.email}",
            }
            return Response({"token": user_token,"user_data":user_data, "message": "Login Successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"errors":{"non_field_errors": ["Username or Password is Invalid!"]}}, status=status.HTTP_404_NOT_FOUND)

class TokenRefreshView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            new_tokens = refresh_tokens(refresh_token)
            return Response(new_tokens, status=status.HTTP_200_OK)
        else:
            return Response({"errors": {"refresh_token_missing": "Refresh token is not provided."}}, status=status.HTTP_400_BAD_REQUEST)
        
        
# ################################################### API to Create User #################################################
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Check if the email already exists
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)
