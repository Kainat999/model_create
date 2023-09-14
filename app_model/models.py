from django.db import models

# Create your models here.
class class_one(models.Model):
    name = models.CharField()
    email = models.EmailField()
    password = models.CharField()
