from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from .models import Music, Artist
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ArtistGetSerializer, ArtistPostSerializer, MusicPostSerializer, MusicGetSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyPageNumberPagination
# User Api View Start.


class MusicAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            query = '''
                SELECT "musicapp_music"."id", "musicapp_music"."artist_id_id",
                       "musicapp_music"."title", "musicapp_music"."album_name",
                       "musicapp_music"."genre", "musicapp_music"."created_at",
                       "musicapp_music"."updated_at"
                FROM "musicapp_music"
                WHERE "musicapp_music"."id" = %s
            '''
            params = (id,)
        else:
            query = '''
                SELECT "musicapp_music"."id", "musicapp_music"."artist_id_id",
                       "musicapp_music"."title", "musicapp_music"."album_name",
                       "musicapp_music"."genre", "musicapp_music"."created_at",
                       "musicapp_music"."updated_at"
                FROM "musicapp_music"
            '''
            params = ()

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()

        musics = []
        for row in result:
            music = {
                'id': row[0],
                'artist_id': row[1],
                'title': row[2],
                'album_name': row[3],
                'genre': row[4],
                'created_at': row[5],
                'updated_at': row[6]
            }
            musics.append(music)

        paginator = self.pagination_class()
        paginated_musics = paginator.paginate_queryset(musics, request)

        return paginator.get_paginated_response(data=paginated_musics)

    def post(self, request, format=None):
        artist_id = request.data.get('artist_id')
        title = request.data.get('title')
        album_name = request.data.get('album_name')
        genre = request.data.get('genre')

        query = '''
            INSERT INTO "musicapp_music" ("artist_id_id", "title", "album_name", "genre")
            VALUES (%s, %s, %s, %s)
        '''
        params = (artist_id, title, album_name, genre)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, format=None):
        id = pk
        artist_id = request.data.get('artist_id')
        title = request.data.get('title')
        album_name = request.data.get('album_name')
        genre = request.data.get('genre')

        query = '''
            UPDATE "musicapp_music"
            SET "artist_id_id" = %s, "title" = %s, "album_name" = %s, "genre" = %s
            WHERE "id" = %s
        '''
        params = (artist_id, title, album_name, genre, id)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_200_OK)

    def patch(self, request, pk=None, format=None):
        id = pk
        artist_id = request.data.get('artist_id')
        title = request.data.get('title')
        album_name = request.data.get('album_name')
        genre = request.data.get('genre')

        query = '''
            UPDATE "musicapp_music"
            SET "artist_id_id" = COALESCE(%s, "artist_id_id"),
                "title" = COALESCE(%s, "title"),
                "album_name" = COALESCE(%s, "album_name"),
                "genre" = COALESCE(%s, "genre")
            WHERE "id" = %s
        '''
        params = (artist_id, title, album_name, genre, id)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        id = pk

        query = '''
            DELETE FROM "musicapp_music"
            WHERE "id" = %s
        '''
        params = (id,)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtistAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            query = '''
                SELECT "musicapp_artist"."id", "musicapp_artist"."name", "musicapp_artist"."dob", 
                       "musicapp_artist"."gender", "musicapp_artist"."csv", "musicapp_artist"."address", 
                       "musicapp_artist"."first_release_year", "musicapp_artist"."no_of_albums_released", 
                       "musicapp_artist"."created_at", "musicapp_artist"."updated_at" 
                FROM "musicapp_artist" 
                WHERE "musicapp_artist"."id" = %s
            '''
            params = (id,)
        else:
            query = '''
                SELECT "musicapp_artist"."id", "musicapp_artist"."name", "musicapp_artist"."dob", 
                       "musicapp_artist"."gender", "musicapp_artist"."csv", "musicapp_artist"."address", 
                       "musicapp_artist"."first_release_year", "musicapp_artist"."no_of_albums_released", 
                       "musicapp_artist"."created_at", "musicapp_artist"."updated_at" 
                FROM "musicapp_artist"
            '''
            params = ()

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()

        artists = []
        for row in result:
            artist = {
                'id': row[0],
                'name': row[1],
                'dob': row[2],
                'gender': row[3],
                'csv': row[4],
                'address': row[5],
                'first_release_year': row[6],
                'no_of_albums_released': row[7],
                'created_at': row[8],
                'updated_at': row[9]
            }
            artists.append(artist)

        paginator = self.pagination_class()
        paginated_artists = paginator.paginate_queryset(artists, request)

        return paginator.get_paginated_response(data=paginated_artists)

    def post(self, request, format=None):
        name = request.data.get('name')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        csv = request.data.get('csv')
        address = request.data.get('address')
        first_release_year = request.data.get('first_release_year')
        no_of_albums_released = request.data.get('no_of_albums_released')

        query = '''
            INSERT INTO "musicapp_artist" ("name", "dob", "gender", "csv", "address",
                                           "first_release_year", "no_of_albums_released")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        params = (name, dob, gender, csv, address,
                  first_release_year, no_of_albums_released)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, format=None):
        id = pk
        name = request.data.get('name')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        csv = request.data.get('csv')
        address = request.data.get('address')
        first_release_year = request.data.get('first_release_year')
        no_of_albums_released = request.data.get('no_of_albums_released')

        query = '''
            UPDATE "musicapp_artist"
            SET "name" = %s, "dob" = %s, "gender" = %s, "csv" = %s, "address" = %s,
                "first_release_year" = %s, "no_of_albums_released" = %s
            WHERE "id" = %s
        '''
        params = (name, dob, gender, csv, address,
                  first_release_year, no_of_albums_released, id)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_200_OK)

    def patch(self, request, pk=None, format=None):
        id = pk
        # Only update the fields that are provided in the request data
        name = request.data.get('name')
        dob = request.data.get('dob')
        gender = request.data.get('gender')
        csv = request.data.get('csv')
        address = request.data.get('address')
        first_release_year = request.data.get('first_release_year')
        no_of_albums_released = request.data.get('no_of_albums_released')

        set_clause = []
        params = []

        if name is not None:
            set_clause.append('"name" = %s')
            params.append(name)
        if dob is not None:
            set_clause.append('"dob" = %s')
            params.append(dob)
        if gender is not None:
            set_clause.append('"gender" = %s')
            params.append(gender)
        if csv is not None:
            set_clause.append('"csv" = %s')
            params.append(csv)
        if address is not None:
            set_clause.append('"address" = %s')
            params.append(address)
        if first_release_year is not None:
            set_clause.append('"first_release_year" = %s')
            params.append(first_release_year)
        if no_of_albums_released is not None:
            set_clause.append('"no_of_albums_released" = %s')
            params.append(no_of_albums_released)

        set_clause_str = ', '.join(set_clause)

        query = f'''
            UPDATE "musicapp_artist"
            SET {set_clause_str}
            WHERE "id" = %s
        '''
        params.append(id)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        id = pk

        query = '''
            DELETE FROM "musicapp_artist"
            WHERE "id" = %s
        '''
        params = (id,)

        with connection.cursor() as cursor:
            cursor.execute(query, params)

        return Response(status=status.HTTP_204_NO_CONTENT)
