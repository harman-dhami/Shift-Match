from django import forms 
from .models import Registration, User
from django.contrib.auth.password_validation import validate_password
class RegistrationForm(forms.ModelForm):
    Choices = (('', ''), ('Air Canada', 'Air Canada'), ('McDonalds', 'McDonalds'))
    
    firstName = forms.CharField(label="First Name:", max_length=100)
    lastName = forms.CharField(label="Last Name:", max_length=100)
    email = forms.EmailField(label="Email:", max_length=100)
    id = forms.ImageField(label="ID:")
    company = forms.ChoiceField(label="Company", choices=Choices)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password:", validators=[validate_password])
    
    class Meta:
        model = Registration 
        fields = ["firstName", "lastName", "email", "id", "company", "password"]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        return cleaned_data
    
class LoginForm(forms.ModelForm):
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password:", max_length=100)
    
    class Meta:
        model = User
        fields = ["email", "password"]
        