from rest_framework import serializers
from .models import Music,Artist
# Create your views here.

class MusicGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'
        
class MusicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'
        

class ArtistGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name','dob','gender','csv','address','first_release_year','no_of_albums_released','created_at','updated_at']    
        
class ArtistPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name','dob','gender','csv','address','first_release_year','no_of_albums_released','created_at','updated_at']