from django.test import TestCase

# Create your tests here.
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserGetSerializer, UserPostSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

# Create your views here.


class UserAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            users = User.objects.get(id=id)
            serializer = UserGetSerializer(users)
            return Response(serializer.data)
        users = User.objects.all()
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        serializer = UserPostSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Complete Data Update'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        serializer = UserPostSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        user = User.objects.get(pk=id)
        user.delete()
        return Response({'msg': 'Data Deleted'})


def create_user(request):
    # Extract user data from the request
    name = request.POST.get('name')
    email = request.POST.get('email')
    print('name', 'email', name, email)

    # Write the SQL query for inserting a new user
    query = "INSERT INTO myapp_user (name, email) VALUES (%s, %s)"
    params = (name, email)

    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, params)

    # Return the API response
    return JsonResponse({'message': 'User created'})


# def get_user(request):
#     # Write the SQL query for retrieving a specific user
#     query = 'SELECT "userapp_customuser"."id", "userapp_customuser"."password", "userapp_customuser"."last_login", "userapp_customuser"."is_superuser", "userapp_customuser"."first_name", "userapp_customuser"."last_name", "userapp_customuser"."is_staff", "userapp_customuser"."is_active", "userapp_customuser"."date_joined", "userapp_customuser"."email", "userapp_customuser"."phone", "userapp_customuser"."dob", "userapp_customuser"."gender", "userapp_customuser"."address", "userapp_customuser"."created_at", "userapp_customuser"."updated_at" FROM "userapp_customuser"', ()
#     # params = (user_id,)
#     # if params is not None:
#     #     with connection.cursor() as cursor:
#     #         # Execute the SQL query
#     #         cursor.execute(query, params)

#     #         # Process the query result
#     #         result = cursor.fetchone()
#     #         print('result',result)
#     with connection.cursor() as cursor:
#         # Execute the SQL query
#         cursor.execute(query)

#         # Process the query result
#         result = cursor.fetchone()
#     print('result',result)
#     if result is None:
#         # Return a 404 Not Found response if the user does not exist
#         return JsonResponse({'error': 'User not found'}, status=404)

#     # Convert the result to a suitable format for the API response
#     user = {
#         'id': result[0],
#         'name': result[1],
#         'email': result[2],
#     }

#     # Return the API response
#     return JsonResponse(user)

from django.http import JsonResponse

def get_user(request):
    # Write the SQL query for retrieving a specific user
    query = 'SELECT "userapp_customuser"."id", "userapp_customuser"."password", "userapp_customuser"."last_login", "userapp_customuser"."is_superuser", "userapp_customuser"."first_name", "userapp_customuser"."last_name", "userapp_customuser"."is_staff", "userapp_customuser"."is_active", "userapp_customuser"."date_joined", "userapp_customuser"."email", "userapp_customuser"."phone", "userapp_customuser"."dob", "userapp_customuser"."gender", "userapp_customuser"."address", "userapp_customuser"."created_at", "userapp_customuser"."updated_at" FROM "userapp_customuser"'

    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query)

        # Process the query result
        result = cursor.fetchall()

    if result is None:
        # Return a 404 Not Found response if the user does not exist
        return JsonResponse({'error': 'User not found'}, status=404)

    # Construct the JSON response
    keys = [
        'id', 'password', 'last_login', 'is_superuser', 'first_name', 'last_name',
        'is_staff', 'is_active', 'date_joined', 'email', 'phone', 'dob', 'gender',
        'address', 'created_at', 'updated_at'
    ]
    users = []
    for row in result:
        user = {}
        for index, key in enumerate(keys):
            user[key] = row[index]
        users.append(user)

    return JsonResponse(users, safe=False)


def update_user(request, user_id):
    # Extract updated user data from the request
    name = request.POST.get('name')
    email = request.POST.get('email')

    # Write the SQL query for updating a user
    query = "UPDATE myapp_user SET name = %s, email = %s WHERE id = %s"
    params = (name, email, user_id)

    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, params)

    # Return the API response
    return JsonResponse({'message': 'User updated'})


def delete_user(request, user_id):
    # Write the SQL query for deleting a user
    query = "DELETE FROM myapp_user WHERE id = %s"
    params = (user_id,)

    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, params)

    # Return the API response
    return JsonResponse({'message': 'User deleted'})
