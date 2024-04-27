from rest_framework import serializers
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ['username','password']
        
######################## User Serializer ##########################
class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')

        user = User(**validated_data)
        user.set_password(password1)
        user.save()
        return user