from django.db import models
from artistmanagement.utils import GENRE_CHOICES, GENDER_CHOICES

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
    
class Music(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE,related_name="musics")
    title = models.CharField(max_length=250)
    album_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
