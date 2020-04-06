from django.contrib import admin

from .models import Post, UserModel

admin.site.register([UserModel, Post])
