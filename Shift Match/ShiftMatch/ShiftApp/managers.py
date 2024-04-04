from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
class UserAccountManager(BaseUserManager):
    def create_user(self, firstName, lastName, username, company, password, employeeId):
        user = self.model(
            firstName=firstName,
            lastName=lastName,
            username=username,
            company=company,
            password=password,
            employeeId=employeeId
        )
        user.save()
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=make_password(password),
            firstName="",
            lastName="",
            company="",
            employeeId=""
        )
        user.is_superuser=True
        user.is_staff=True
        user.is_admin=True
        user.is_active=True
        user.save()
        return user