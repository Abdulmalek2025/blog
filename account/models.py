from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    job = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    picture = models.ImageField(upload_to='profiles/')
