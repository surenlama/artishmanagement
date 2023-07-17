from django.db import models
from artistmanagement.utils import GENRE_CHOICES, GENDER_CHOICES
from django.core.exceptions import ValidationError
import datetime
# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=250)   
    dob = models.DateTimeField(null=True)
    gender = models.CharField(max_length=250, choices=GENDER_CHOICES)
    address = models.CharField(max_length=250)
    first_release_year = models.DateField()
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return ""+str(self.id)
    
    def dict(self):
            return {
                'name': self.name,
                'dob': self.dob,
                'gender': self.gender,
                'address': self.address,
                'first_release_year': self.first_release_year,
                'no_of_albums_released': self.no_of_albums_released,
            } 
 
    
class Music(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE,related_name="musics")
    title = models.CharField(max_length=250)
    album_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_media')