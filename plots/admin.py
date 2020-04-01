from django.contrib import admin

# Register your models here.
from .models import UserModel, Post

admin.site.register([UserModel, Post])
