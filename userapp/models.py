from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from artistmanagement.utils import GENDER_CHOICES
from userapp.manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=250,null=True)
    dob = models.DateTimeField(null=True)
    gender = models.CharField(max_length=250,choices=GENDER_CHOICES,null=True)  
    address = models.CharField(max_length=250,null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


        # Perform custom validation here
       
