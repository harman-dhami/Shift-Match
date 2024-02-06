from django.db import models
from django import forms

class Registration(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userId = models.ImageField()
    userPassword = models.CharField(max_length=100)
    
class User(models.Model):
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)
    
class Admin(models.Model):
    userName = models.CharField(max_length=20)
    adminPassword = models.CharField(max_length=100)
    
class IdRequest(models.Model):
    userID = models.ImageField()
    decision = models.CharField(max_length=100)
    
