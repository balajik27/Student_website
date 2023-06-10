from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Subject(models.Model):
    name = models.CharField(max_length=100 , blank=False , null= True)
    description = models.TextField(max_length=200,blank=True)
    def __str__(self):
        return self.name

class File(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE) #, related_name='files'
    file = models.FileField(upload_to="files/%Y/%m/%d",default=None)

    def __str__(self):
        return self.file.name
    
class Image(models.Model):
    sub = models.ForeignKey(Subject, on_delete=models.CASCADE)#,related_name = 'images'
    image = models.ImageField(upload_to='images/%Y/%m/%d', default=None)

    def __str__(self):
        return self.image.name

class User_Details(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    mobile = models.IntegerField()
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Hack(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    def __str__(self):
        return self.name

class Announce(models.Model):
    title = models.CharField(max_length=50, default="Announcement")
    text = models.CharField(max_length=200)
    currentdate= models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title