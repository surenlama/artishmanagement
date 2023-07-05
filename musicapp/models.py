from django.db import models
from artistmanagement.utils import GENRE_CHOICES, GENDER_CHOICES

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=250)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=250, choices=GENDER_CHOICES)
    csv = models.FileField(upload_to="csv",null=True)
    address = models.CharField(max_length=250)
    first_release_year = models.DateField()
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class Music(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    album_name = models.CharField(max_length=250)
    genre = models.CharField(max_length=250, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
