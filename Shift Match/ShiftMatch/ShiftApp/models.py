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
    qualifications = models.CharField(max_length=100,  default="Basic")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    
    objects=UserAccountManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
#class Login(models.Model):
    #userEmail = models.EmailField()
    #userPassword = models.CharField(max_length=100)
    
class Shifts(models.Model):
    shiftStart = models.DateTimeField()
    shiftEnd = models.DateTimeField()
    hours = models.IntegerField(default=0)
    dateAvailable = models.DateField(default="2024-01-01")
    ShiftPool = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    Matching =  models.BooleanField(default=False)
    moneyAmount = models.CharField(max_length=10, default=0)
    qualification = models.CharField(max_length=100, default="None")
    location = models.CharField(max_length=100, default="YVR")
    locationNotWillingToWork = models.CharField(max_length=100, default="None")
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    
class Admin(models.Model):
    userName = models.CharField(max_length=20)
    adminPassword = models.CharField(max_length=100)
    
class IdRequest(models.Model):
    userID = models.CharField(max_length=100)
    decision = models.CharField(max_length=100)
    
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(blank=True, null=True, max_length=225)
    status = models.CharField(blank=True, null=True, max_length=225)
    channel = models.CharField(max_length=100, default="my_channel")