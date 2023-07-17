from django.db import connection
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer, UserRegisterSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyPageNumberPagination
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.utils import timezone

current_datetime = timezone.now()


# User Api View Start.


User = get_user_model()


class UserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            query = 'SELECT "userapp_customuser"."id", "userapp_customuser"."password", "userapp_customuser"."last_login", "userapp_customuser"."is_superuser", "userapp_customuser"."first_name", "userapp_customuser"."last_name", "userapp_customuser"."is_staff", "userapp_customuser"."is_active", "userapp_customuser"."date_joined", "userapp_customuser"."email", "userapp_customuser"."phone", "userapp_customuser"."dob", "userapp_customuser"."gender", "userapp_customuser"."address", "userapp_customuser"."created_at", "userapp_customuser"."updated_at" FROM "userapp_customuser" WHERE "userapp_customuser"."id" = %s'
            params = (id,)
        else:
            query = 'SELECT "userapp_customuser"."id", "userapp_customuser"."password", "userapp_customuser"."last_login", "userapp_customuser"."is_superuser", "userapp_customuser"."first_name", "userapp_customuser"."last_name", "userapp_customuser"."is_staff", "userapp_customuser"."is_active", "userapp_customuser"."date_joined", "userapp_customuser"."email", "userapp_customuser"."phone", "userapp_customuser"."dob", "userapp_customuser"."gender", "userapp_customuser"."address", "userapp_customuser"."created_at", "userapp_customuser"."updated_at" FROM "userapp_customuser"'
            params = ()

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query, params)

            # Process the query result
            result = cursor.fetchall()

        users = []
        for row in result:
            # Create a dictionary for each user
            user = {
                'id': row[0],
                'password': row[1],
                'last_login': row[2],
                'is_superuser': row[3],
                'first_name': row[4],
                'last_name': row[5],
                'is_staff': row[6],
                'is_active': row[7],
                'date_joined': row[8],
                'email': row[9],
                'phone': row[10],
                'dob': row[11],
                'gender': row[12],
                'address': row[13],
                'created_at': row[14],
                'updated_at': row[15]
            }
            users.append(user)
        paginator = self.pagination_class()
        paginated_musics = paginator.paginate_queryset(users, request)

        return paginator.get_paginated_response(data=paginated_musics)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            query = 'INSERT INTO "userapp_customuser" ("password",  "is_superuser",\
            "first_name", "last_name", "is_staff", "is_active", "date_joined", \
            "email","phone", "dob", "gender", "address", "created_at") \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            # Extract the data from the request
            password = make_password(request.data.get('password'))  # Hash the password
            is_superuser = True
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            is_staff = True
            is_active = True
            date_joined = current_datetime
            email = request.data.get('email')
            phone = request.data.get('phone')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            address = request.data.get('address')
            created_at = current_datetime
            print(password,is_superuser,first_name,last_name,is_staff,is_active,date_joined,email,phone, dob, gender, address, created_at)

            params = (password, is_superuser, first_name, last_name, is_staff,is_active, date_joined, email, phone, dob, gender, address, created_at)

            with connection.cursor() as cursor:
                # Execute the SQL query with parameters
                cursor.execute(query, params)
                user_id = cursor.lastrowid

            # Retrieve the user object
            user = User.objects.get(pk=user_id)

            # Create a token for the user
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            id = pk
            query = '''
                UPDATE "userapp_customuser"
                SET "password" = %s,
                    "is_superuser" = %s,
                    "first_name" = %s,
                    "last_name" = %s,
                    "is_staff" = %s,
                    "is_active" = %s,
                    "date_joined" = %s,
                    "email" = %s,
                    "phone" = %s,
                    "dob" = %s,
                    "gender" = %s,
                    "address" = %s,
                    "updated_at" = %s
                WHERE "id" = %s
            '''

            # Extract the data from the request
            password = request.data.get('password')
            is_superuser = True
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            is_staff = True
            is_active = True
            date_joined = current_datetime
            email = request.data.get('email')
            phone = request.data.get('phone')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            address = request.data.get('address')
            updated_at = current_datetime

            params = (password, is_superuser, first_name, last_name, is_staff, is_active,
                      date_joined, email, phone, dob, gender, address, updated_at, id)

            with connection.cursor() as cursor:
                # Execute the SQL query with parameters
                cursor.execute(query, params)

            return Response({'msg': 'User Updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            id = pk
            query = '''
                UPDATE "userapp_customuser"
                SET "password" = COALESCE(%s, "userapp_customuser"."password"),
                    "is_superuser" = COALESCE(%s, "userapp_customuser"."is_superuser"),
                    "first_name" = COALESCE(%s, "userapp_customuser"."first_name"),
                    "last_name" = COALESCE(%s, "userapp_customuser"."last_name"),
                    "is_staff" = COALESCE(%s, "userapp_customuser"."is_staff"),
                    "is_active" = COALESCE(%s, "userapp_customuser"."is_active"),
                    "date_joined" = COALESCE(%s, "userapp_customuser"."date_joined"),
                    "email" = COALESCE(%s, "userapp_customuser"."email"),
                    "phone" = COALESCE(%s, "userapp_customuser"."phone"),
                    "dob" = COALESCE(%s, "userapp_customuser"."dob"),
                    "gender" = COALESCE(%s, "userapp_customuser"."gender"),
                    "address" = COALESCE(%s, "userapp_customuser"."address"),
                    "updated_at" = COALESCE(%s, "userapp_customuser"."updated_at")
                WHERE "id" = %s
            '''

            # Extract the data from the request
            password = request.data.get('password')
            is_superuser = True
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            is_staff = True
            is_active = True
            date_joined = current_datetime
            email = request.data.get('email')
            phone = request.data.get('phone')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            address = request.data.get('address')
            updated_at = request.data.get('updated_at')

            params = (password, is_superuser, first_name, last_name, is_staff, is_active,
                      date_joined, email, phone, dob, gender, address, updated_at, id)

            with connection.cursor() as cursor:
                # Execute the SQL query with parameters
                cursor.execute(query, params)

            return Response({'msg': 'User Updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        id = pk
        # Delete the user
        user_query = 'DELETE FROM userapp_customuser WHERE id = %s'
        user_params = (id,)

        try:
            with connection.cursor() as cursor:
                cursor.execute(user_query, user_params)
                return Response({'msg': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            print('enter')
            if id:
                user = User.objects.get(id=id)
                user.delete()
                return Response({'msg': 'User Deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            password = make_password(request.data.get(
                'password'))  # Hash the password
            print('email', email)
            query = '''
                INSERT INTO userapp_customuser (email, password, is_superuser,first_name,last_name,\
                    is_staff,is_active,date_joined)
                VALUES (%s, %s, %s,%s,%s,%s,%s,%s)
            '''
            params = (email, password, False, '', '',
                      True, True, current_datetime)

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            user = User.objects.get(email=email)
            token = Token.objects.create(user=user)

            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
