from django.contrib.auth.models import BaseUserManager

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