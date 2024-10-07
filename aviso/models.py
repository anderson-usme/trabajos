from django.db import models
from .views import check_url 


# Create your models here.

class Project(models.Model):
    url = models.URLField(check_url)
    name = models.TextField(max_length=200)
    location = models.TextField(max_length=200)

