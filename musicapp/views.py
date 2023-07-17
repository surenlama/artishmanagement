from django.db import connection
from django.http import HttpResponse
from .models import  Artist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .mypaginations import MyPageNumberPagination
from django.db import IntegrityError
from django.utils import timezone
import os
import csv
import datetime
import csv
from .serializer import MusicSerializer,ArtistSerializer,CSVSerializer
# User Api View Start.
current_datetime = timezone.now()


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
        serializer = MusicSerializer(data=request.data)

        if serializer.is_valid():       
       
            artist_id = request.data.get('artist_id')
            title = request.data.get('title')
            album_name = request.data.get('album_name')
            genre = request.data.get('genre')
            created_at = timezone.now()  

            query = '''
                INSERT INTO "musicapp_music" ("artist_id_id", "title", "album_name", "genre","created_at")
                VALUES (%s, %s, %s, %s, %s)
            '''
            params = (artist_id, title, album_name, genre, created_at)

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():    
            id = pk
            artist_id = request.data.get('artist_id')
            title = request.data.get('title')
            album_name = request.data.get('album_name')
            genre = request.data.get('genre')
            updated_at = timezone.now()  # Get the current datetime

            query = '''
                UPDATE "musicapp_music"
                SET "artist_id_id" = %s, "title" = %s, "album_name" = %s, "genre" = %s, "updated_at" = %s
                WHERE "id" = %s
            '''
            params = (artist_id, title, album_name, genre, updated_at, id)

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
    def patch(self, request, pk=None, format=None):
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():    
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
        
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
                       "musicapp_artist"."gender", "musicapp_artist"."address", 
                       "musicapp_artist"."first_release_year", "musicapp_artist"."no_of_albums_released", 
                       "musicapp_artist"."created_at", "musicapp_artist"."updated_at" 
                FROM "musicapp_artist" 
                WHERE "musicapp_artist"."id" = %s
            '''
            params = (id,)
        else:
            query = '''
                SELECT "musicapp_artist"."id", "musicapp_artist"."name", "musicapp_artist"."dob", 
                       "musicapp_artist"."gender", "musicapp_artist"."address", 
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
                'address': row[4],
                'first_release_year': row[5],
                'no_of_albums_released': row[6],
                'created_at': row[7],
                'updated_at': row[8]
            }
            artists.append(artist)
        paginator = self.pagination_class()
        paginated_musics = paginator.paginate_queryset(artists, request)

        return paginator.get_paginated_response(data=paginated_musics)


    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data)

        if serializer.is_valid():       
        
            name = request.data.get('name')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            address = request.data.get('address')
            first_release_year = request.data.get('first_release_year')
            no_of_albums_released = request.data.get('no_of_albums_released')
            created_at = timezone.now()  # Get the current datetime

            query = '''
                INSERT INTO "musicapp_artist" ("name", "dob", "gender", "address",
                                            "first_release_year", "no_of_albums_released","created_at")
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            '''
            params = (name, dob, gender, address,
                    first_release_year, no_of_albums_released,created_at)

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    def put(self, request, pk=None, format=None):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():   
            id = pk
            name = request.data.get('name')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
            address = request.data.get('address')
            first_release_year = request.data.get('first_release_year')
            no_of_albums_released = request.data.get('no_of_albums_released')
            updated_at = timezone.now()  # Get the current datetime

            query = '''
                UPDATE "musicapp_artist"
                SET "name" = %s, "dob" = %s, "gender" = %s, "address" = %s,
                    "first_release_year" = %s, "no_of_albums_released" = %s,
                    "updated_at" = %s  -- Update the updated_at field
                WHERE "id" = %s
            '''
            params = (name, dob, gender, address,
                    first_release_year, no_of_albums_released, updated_at, id)

            with connection.cursor() as cursor:
                cursor.execute(query, params)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
    def patch(self, request, pk=None, format=None):
        serializer = ArtistSerializer(data=request.data)

        if serializer.is_valid():   
            id = pk
            # Only update the fields that are provided in the request data
            name = request.data.get('name')
            dob = request.data.get('dob')
            gender = request.data.get('gender')
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def delete(self, request, pk=None, format=None):
        query = '''
            DELETE FROM musicapp_artist
            WHERE id = %s
        '''
        params = (pk,)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return Response("Artist deleted successfully")
        except IntegrityError:
            return Response("Cannot delete artist. Associated music exists.", status=400)
        
        


class ArtistMusicAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            query = '''
                SELECT "musicapp_artist"."id", "musicapp_artist"."name", "musicapp_artist"."dob", 
                       "musicapp_artist"."gender", "musicapp_artist"."address", 
                       "musicapp_artist"."first_release_year", "musicapp_artist"."no_of_albums_released", 
                       "musicapp_artist"."created_at", "musicapp_artist"."updated_at",
                       "musicapp_music"."id", "musicapp_music"."title", "musicapp_music"."album_name", 
                       "musicapp_music"."genre", "musicapp_music"."created_at", "musicapp_music"."updated_at"
                FROM "musicapp_artist"
                LEFT JOIN "musicapp_music" ON "musicapp_music"."artist_id_id" = "musicapp_artist"."id"
                WHERE "musicapp_artist"."id" = %s
            '''
            params = (id,)
        else:
            query = '''
                SELECT "musicapp_artist"."id", "musicapp_artist"."name", "musicapp_artist"."dob", 
                       "musicapp_artist"."gender", "musicapp_artist"."address", 
                       "musicapp_artist"."first_release_year", "musicapp_artist"."no_of_albums_released", 
                       "musicapp_artist"."created_at", "musicapp_artist"."updated_at",
                       "musicapp_music"."id", "musicapp_music"."title", "musicapp_music"."album_name", 
                       "musicapp_music"."genre", "musicapp_music"."created_at", "musicapp_music"."updated_at"
                FROM "musicapp_artist"
                LEFT JOIN "musicapp_music" ON "musicapp_music"."artist_id_id" = "musicapp_artist"."id"
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
                'address': row[4],
                'first_release_year': row[5],
                'no_of_albums_released': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'musics': []
            }
            if row[9]:
                music = {
                    'id': row[9],
                    'title': row[10],
                    'album_name': row[11],
                    'genre': row[12],
                    'created_at': row[13],
                    'updated_at': row[14]
                }
                artist['musics'].append(music)
            artists.append(artist)

        return Response(artists)




def save_uploaded_file(request, file_name):
    file_path = os.path.join('csv_media', file_name)
    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[3] == 'first_release_year':
                continue
            artist = Artist(
                name=row[0],
                gender=row[1],
                address=row[2],
                first_release_year=datetime.date.fromisoformat(row[3].strip()),
                no_of_albums_released=row[4],
            )

            # if Artist.objects.filter(address=artist.name).exists():
            #     continue
            Artist.objects.create(**artist.dict())

class CSVFileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = CSVSerializer(data=request.data)
        if serializer.is_valid():       
            csv_file = request.data['file']
            print('csv_file',csv_file)
            file_name = csv_file.name
            file_path = save_uploaded_file(request, file_name)

            if file_path:
                query = '''
        INSERT INTO artistapp_csvfile (file)
        VALUES (%s)
    '''
                params = (file_name,)

                with connection.cursor() as cursor:
                    if cursor.execute(query, params):
                        data = {'file_name': file_name}
                        return Response(data=data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


class ArtistCSVView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        artist_objects = Artist.objects.all()
        print('called me ',artist_objects)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="artist.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Date of Birth', 'Gender', 'Address', 'First Release Year', 'No. of Albums Released', 'Created At', 'Updated At'])

        for artist in artist_objects:
            writer.writerow([
                artist.id,
                artist.name,
                artist.dob,
                artist.gender,
                artist.address,
                artist.first_release_year,
                artist.no_of_albums_released,
                artist.created_at,
                artist.updated_at
            ])
        print('response11',response)
        return response