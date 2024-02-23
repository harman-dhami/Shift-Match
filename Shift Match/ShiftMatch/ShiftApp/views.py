from django.shortcuts import render, redirect
import pymongo
from django.core.mail import send_mail
from .models import Registration
from .forms import RegistrationForm, LoginForm, AdminLogin, IDRequest
from django.contrib import messages
from .settings import EMAIL_HOST_USER

myclient = pymongo.MongoClient("mongodb+srv://user01:WAX5VkFPgLmrclRt@shiftmatch.mux73es.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["ShiftMatch"]
mycol = mydb["users"]


def registration(request):
    global id
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            userEmail = form.cleaned_data['email']
            id = form.cleaned_data['id']
            company = form.cleaned_data['company']
            userPassword = form.cleaned_data['password']
            
                
            if (idRequest == 'Deny'):
                subject = 'ShiftMatch Account Request'
                message = f'Hello' +firstName+ ', your identification has not been approved due to criteria requirements. Please register again for another ID approval request. Thanks'
                email_from = EMAIL_HOST_USER
                recipient = userEmail
                send_mail(subject, message, email_from, recipient)
            else:
                mydict = { "Firstname": firstName, "Lastname": lastName, "Email": userEmail , "ID": id, "Company": company, "Password": userPassword}
                x = mycol.insert_one(mydict)
    else:
        form = RegistrationForm()
    return render(request, "Registration.html", {"form": form})

def login(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            userName = form.cleaned_data['email']
            userPassword = form.cleaned_data['password']
            
            dbpwd = mydb.users.find_one({"Email": userName}, {"Password": 1, "_id": 0})
            dbemail = mydb.users.find_one({"Email": userName})
            adminpwd = mydb.Admins.find_one({"userName": userName}, {"password": 1, "_id": 0})
            adminName = mydb.Admins.find_one({"userName": userName})
            
            if (dbemail != None):
                if (dbpwd.get("Password") != userPassword):
                    return render(request, "Login.html", {"form": form})
                else:
                    return render(request, "Dashboard.html")
            elif (adminName != None):
                if (adminpwd.get("password") != userPassword):
                    return render(request, "Login.html", {"form": form})
                else:
                    return render(request, "AdminPage.html")
                
    else:
        form = LoginForm()
    return render(request, "Login.html", {"form": form})

def adminLogin(request):
        return render(request, "AdminPage.html")
    
def idRequest(request):
    if (id != None):
        return render (request, 'AdminPage.html',{"id": id})
    
    form = IDRequest(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            requestDecision = form.cleaned_data['decision']
            
            return requestDecision
        
def calendarShiftInput(request):
    
    return render(request, "Dashboard.html")
            