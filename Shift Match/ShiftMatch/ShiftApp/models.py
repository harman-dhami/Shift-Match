from django.db import models
from django import forms

class Registration(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)
    confirmPassword = models.CharField(max_length=100)
    
class User(models.Model):
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)
