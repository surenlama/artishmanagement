from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import Token
from django.contrib.auth.hashers import make_password

# Create your views here.
User = get_user_model()


class UserGetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'address', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Hash the password using make_password()
        hashed_password = make_password(password)
        # Add the hashed password back to the validated_data
        validated_data['password'] = hashed_password

        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
