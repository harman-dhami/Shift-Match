from django import forms 
from .models import User, Admin, IdRequest, Shifts
from django.contrib.auth.password_validation import validate_password

class RegistrationForm(forms.ModelForm):
    Choices = (('', ''), ('Air Canada', 'Air Canada'), ('McDonalds', 'McDonalds'))
    
    firstName = forms.CharField(label="First Name:", max_length=100, widget=forms.TextInput(attrs={'class': 'firstNameClass'}))
    lastName = forms.CharField(label="Last Name:", max_length=100)
    email = forms.CharField(label="Email:", max_length=100)
    id = forms.CharField(label="ID Number:", max_length=100)
    company = forms.ChoiceField(label="Company", choices=Choices)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password:", validators=[validate_password])
    
    class Meta:
        model = User 
        fields = ["firstName", "lastName", "email", "id", "company", "password"]
    
class LoginForm(forms.ModelForm):
    email = forms.EmailField(label="Email:", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password:", max_length=100)
    
    class Meta:
        model = User
        fields = ["email", "password"]
        

class AdminLogin(forms.ModelForm):
    userName = forms.CharField(label="Username:", max_length=20)
    adminPassword = forms.CharField(widget=forms.PasswordInput(), label="Password:")
    
    class Meta:
        model = Admin
        fields = ["userName", "adminPassword"]
        
class IDRequest(forms.ModelForm):
   
    Choices = (('Please Select', 'Please Select'), ('Accept', 'Accept'), ('Deny', 'Deny'))
    id = forms.CharField(label = "ID Number:", max_length=100)
    decision = forms.ChoiceField(label = "Decision:", choices = Choices)
    
    class Meta:
        model = IdRequest
        fields = ["id", "decision"]
        
class ShiftPoolForm(forms.ModelForm):
    
    
    shift = forms.DateField(label="Select Shift Date", widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}), input_formats=["%Y-%m-%d"])
    daysAvailabletoWork = forms.DateField(label="Dates Willing To Work", widget= forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}), input_formats=["%Y-%m-%d"])
    class Meta:
        model = Shifts
        fields = ["shift", "daysAvailabletoWork"]
    
    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username')
        super(ShiftPoolForm, self).__init__(*args, **kwargs)
        self.fields['shift'].queryset = Shifts.objects.filter(username = username).filter(ShiftPool = False)
        
class AddShiftForm(forms.ModelForm):
    hours = forms.CharField(label="Hours:", max_length=100)
    
    class Meta:
        model = Shifts
        fields = ["shiftStart", "shiftEnd", "hours"]

        widgets = {
            "shiftStart":forms.TextInput(attrs={'type':'datetime-local' }),
            "shiftEnd":forms.TextInput(attrs={'type':'datetime-local' })
        }