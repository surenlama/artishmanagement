from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import Token
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from artistmanagement.utils import GENDER_CHOICES
from datetime import date
# Create your views here.
User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'address', 'password']
        read_only_fields = ['id']

    def validate_dob(self, value):
        if value and value.date() >= date.today():
            raise serializers.ValidationError('Date of birth must be in the past.')
        return value

    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('First name should  be more than 2 characters.')
        return value
        
    def validate_phone(self, value):
        if value:
            if not value.isnumeric() or len(value) != 10:
                raise serializers.ValidationError("phone number must have length 10 with numeric.")
        return value

   
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already Used.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    
    
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'address', 'password']
        read_only_fields = ['id']
        
    def validate_dob(self, value):
        if value and value.date() >= date.today():
            raise serializers.ValidationError('Date of birth must be in the past.')
        return value

    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('First name should  be more than 2 characters.')
        return value
        
    def validate_phone(self, value):
        if value:
            if not value.isnumeric() or len(value) != 10:
                raise serializers.ValidationError("phone number must have length 10 with numeric.")
        return value

   
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already Used.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value