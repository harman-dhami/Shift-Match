from django.shortcuts import render
from django.template.response import TemplateResponse
import pymongo
from django.core.mail import send_mail
from .models import Registration
from .forms import RegistrationForm, LoginForm, AdminLogin
from django.contrib import messages

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
                
            if (id == True):
                return TemplateResponse(request, "AdminPage.html", {"id": id})
        
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
            dbemail = mydb.users.find_one({"Email": userEmail})
            
            if (dbemail == None):
                print("Email does not exist")
            elif (dbpwd.get("password") != userPassword):
                print("Wrong password/email")
            else:
                print("Successful Login")
    return render(request, "Login.html", {"form": form})

def adminLogin(request):
    form = AdminLogin(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userName = form.cleaned_data['userName']
            adminPassword = form.cleaned_data['adminPassword']
            
            adminpwd = mydb.Admins.find_one({"userName": userName}, {"password": 1, "_id": 0})
            adminName = mydb.Admins.find_one({"userName": userName})
            
            
            if (adminName == None):
                return render(request, "AdminLogin.html", {"form": form, "htmltext": "Username Does Not Exist!"})
            elif (adminpwd.get("password") != adminPassword):
                return render(request, "AdminLogin.html", {"form": form, "htmltext": "Incorrect Username/Password"})
            else:
                return render(request, "AdminPage.html")
            
    return render(request, "AdminLogin.html", {"form": form})
    
def idRequest():
    return
            