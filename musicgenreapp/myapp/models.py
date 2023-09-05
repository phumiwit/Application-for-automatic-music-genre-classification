from django.db import models
from django import forms
from django.contrib.auth.models import User
from jsonfield import JSONField


class Userdata(models.Model):
    UserName = models.CharField(max_length = 20)
    FirstName = models.CharField(max_length = 20)
    LastName = models.CharField(max_length = 20)
    Age = models.IntegerField()
    Email = models.EmailField(max_length=254)
    Date = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.FirstName + "," + self.LastName

class Audio(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    Filename = models.CharField(max_length=254)
    Genre = models.CharField(max_length=100, null=True, blank=True)
    Top3_Genre = models.CharField(max_length=255, null=True, blank=True)
    Value = Value = JSONField()
    

class Collection(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    FileName = models.CharField(max_length=255)
    Genre = models.CharField(max_length=255)
    Top3_Genre = models.CharField(max_length=255, null=True, blank=True)
    Audio_Id = models.CharField(max_length=255)
    CollectionName = models.CharField(max_length=255, null=True, blank=True)
    
    
class File(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    FileName = models.CharField(max_length=250)
    FileUrl = models.FileField(upload_to='uploads/')
    

class Valueforchart(models.Model):
    Genre = models.CharField(max_length=255, null=True, blank=True)
    Age = models.IntegerField(null=True, blank=True)
