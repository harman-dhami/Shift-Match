from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserAccountManager
from multiselectfield import MultiSelectField

class User(AbstractBaseUser):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    employeeId = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default="password12r")
    role = models.CharField(max_length=100,  default="Basic")
    USERNAME_FIELD = "username"
    
    objects=UserAccountManager()
    
#class Login(models.Model):
    #userEmail = models.EmailField()
    #userPassword = models.CharField(max_length=100)
    
class Shifts(models.Model):
    shiftStart = models.DateTimeField()
    shiftEnd = models.DateTimeField()
    hours = models.IntegerField()
    dateAvailable = models.DateField(default="2024-01-01")
    ShiftPool = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    username = models.ForeignKey(User, on_delete=models.PROTECT, to_field="username")
    
class Admin(models.Model):
    userName = models.CharField(max_length=20)
    adminPassword = models.CharField(max_length=100)
    
class IdRequest(models.Model):
    userID = models.CharField(max_length=100)
    decision = models.CharField(max_length=100)