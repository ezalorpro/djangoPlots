from django.db import models

# Create your models here.

class PlotsLy(models.Model):
    x_points = models.TextField(max_length=1000, default="[0, 1, 2]")
    y_points = models.TextField(max_length=1000, default="[0, 1, 2]")
