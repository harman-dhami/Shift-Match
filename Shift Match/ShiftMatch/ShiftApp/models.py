from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserAccountManager

class User(AbstractBaseUser):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    employeeId = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default="password12r")
    USERNAME_FIELD = "username"
    
    objects=UserAccountManager()
    
class Login(models.Model):
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)
    
class Admin(models.Model):
    userName = models.CharField(max_length=20)
    adminPassword = models.CharField(max_length=100)
    
class IdRequest(models.Model):
    userID = models.CharField(max_length=100)
    decision = models.CharField(max_length=100)