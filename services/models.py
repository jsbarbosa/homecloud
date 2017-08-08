import os
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)

    profile_pic = models.ImageField(blank = True)

    files = []

    def __str__(self):
        return self.user.username
