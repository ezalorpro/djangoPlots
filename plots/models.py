from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='plots', default='plots/default.jpg')
    location = models.CharField(max_length=140)
    gender = models.CharField(max_length=140)
    information = models.TextField()

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)
