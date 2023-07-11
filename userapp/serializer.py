from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import Token
from django.contrib.auth.hashers import make_password

# Create your views here.
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','email', 'password']


    
    
class UserGetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'address', 'password']


