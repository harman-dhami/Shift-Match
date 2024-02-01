from django.shortcuts import render
import pymongo
from django.core.mail import send_mail
from .models import Registration
from .forms import RegistrationForm, LoginForm

myclient = pymongo.MongoClient("mongodb+srv://user01:WAX5VkFPgLmrclRt@shiftmatch.mux73es.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["ShiftMatch"]
mycol = mydb["users"]

def registration(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            userEmail = form.cleaned_data['email']
            id = form.cleaned_data['id']
            company = form.cleaned_data['company']
            userPassword = form.cleaned_data['password']
            
        
            mydict = { "Firstname": firstName, "Lastname": lastName, "Email": userEmail , "ID": id, "Company": company, "Password": userPassword}
            x = mycol.insert_one(mydict)
    else:
        form = RegistrationForm()
    return render(request, "Registration.html", {"form": form})

def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userEmail = form.cleaned_data['email']
            userPassword = form.cleaned_data['password']
            
            dbpwd = mydb.users.find_one({"Email": userEmail}, {"Password": 1, "_id": 0})
            
            if (dbpwd.get("Password") == userPassword):
                print("Login")
            else:
                print("Fail")
    return render(request, "Login.html", {"form": form})