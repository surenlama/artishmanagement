from django.db import connection
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserGetSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyPageNumberPagination
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

# User Api View Start.


User = get_user_model()


class UserAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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
        paginator = MyPageNumberPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserGetSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        query = 'INSERT INTO "userapp_customuser" ("password", "last_login", "is_superuser", "first_name", "last_name", "is_staff", "is_active", "date_joined", "email", "phone", "dob", "gender", "address", "created_at", "updated_at") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

        # Extract the data from the request
        password = make_password(request.data.get('password'))  # Hash the password
        last_login = request.data.get('last_login')
        is_superuser = request.data.get('is_superuser')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        is_staff = request.data.get('is_staff')
        is_active = request.data.get('is_active')
        date_joined = request.data.get('date_joined')
        email = request.data.get('email')
        phone = request.data.get('phone')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        address = request.data.get('address')
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')

        params = (password, last_login, is_superuser, first_name, last_name, is_staff,
                  is_active, date_joined, email, phone, dob, gender, address, created_at, updated_at)

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query, params)
            user_id = cursor.lastrowid

        # Retrieve the user object
        user = User.objects.get(pk=user_id)

        # Create a token for the user
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        id = pk
        query = '''
            UPDATE "userapp_customuser"
            SET "password" = %s,
                "last_login" = %s,
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
                "created_at" = %s,
                "updated_at" = %s
            WHERE "id" = %s
        '''

        # Extract the data from the request
        password = request.data.get('password')
        last_login = request.data.get('last_login')
        is_superuser = request.data.get('is_superuser')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        is_staff = request.data.get('is_staff')
        is_active = request.data.get('is_active')
        date_joined = request.data.get('date_joined')
        email = request.data.get('email')
        phone = request.data.get('phone')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        address = request.data.get('address')
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')

        params = (password, last_login, is_superuser, first_name, last_name, is_staff, is_active,
                  date_joined, email, phone, dob, gender, address, created_at, updated_at, id)

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query, params)

        return Response({'msg': 'User Updated'})

    def patch(self, request, pk, format=None):
        id = pk
        query = '''
            UPDATE "userapp_customuser"
            SET "password" = COALESCE(%s, "userapp_customuser"."password"),
                "last_login" = COALESCE(%s, "userapp_customuser"."last_login"),
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
                "created_at" = COALESCE(%s, "userapp_customuser"."created_at"),
                "updated_at" = COALESCE(%s, "userapp_customuser"."updated_at")
            WHERE "id" = %s
        '''

        # Extract the data from the request
        password = request.data.get('password')
        last_login = request.data.get('last_login')
        is_superuser = request.data.get('is_superuser')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        is_staff = request.data.get('is_staff')
        is_active = request.data.get('is_active')
        date_joined = request.data.get('date_joined')
        email = request.data.get('email')
        phone = request.data.get('phone')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        address = request.data.get('address')
        created_at = request.data.get('created_at')
        updated_at = request.data.get('updated_at')

        params = (password, last_login, is_superuser, first_name, last_name, is_staff, is_active,
                  date_joined, email, phone, dob, gender, address, created_at, updated_at, id)

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query, params)

        return Response({'msg': 'User Updated'})

    def delete(self, request, pk, format=None):
        id = pk
        query = 'DELETE FROM "userapp_customuser" WHERE "id" = %s'
        params = (id,)

        with connection.cursor() as cursor:
            # Execute the SQL query with parameters
            cursor.execute(query, params)

        return Response({'msg': 'User Deleted'})
