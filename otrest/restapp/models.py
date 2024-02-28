from django.db import models

# Create your models here.
class Info(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=15)
    degree = models.CharField(max_length=20)