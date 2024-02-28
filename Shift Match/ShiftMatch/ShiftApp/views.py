from django.shortcuts import render, redirect
import pymongo
from django.core.mail import send_mail
from .models import User
from .forms import RegistrationForm, LoginForm, AdminLogin, IDRequest
from django.contrib import messages
from .settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

myclient = pymongo.MongoClient("mongodb+srv://user01:WAX5VkFPgLmrclRt@shiftmatch.mux73es.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["ShiftMatch"]
mycol = mydb["users"]


def registration(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            userEmail = form.cleaned_data['email']
            employeeId = form.cleaned_data['id']
            company = form.cleaned_data['company']
            userPassword = form.cleaned_data['password']
            userPassword1 = make_password(userPassword)
            user = User.objects.create_user(firstName=firstName, lastName=lastName, username=userEmail, employeeId=employeeId, company=company, password=userPassword1)
            user.is_active = True
            user.save()
            
                
            if (idRequest == 'Deny'):
                subject = 'ShiftMatch Account Request'
                message = f'Hello' +user.firstName+ ', your identification has not been approved due to criteria requirements. Please register again for another ID approval request. Thanks'
                email_from = EMAIL_HOST_USER
                recipient = user.userEmail
                send_mail(subject, message, email_from, recipient)
            else:
                #mydict = { "Firstname": user.firstName, "Lastname": user.lastName, "Email": user.username , "ID": user.employeeId, "Company": user.company, "Password": user.userPassword}
                #x = mycol.insert_one(mydict)
                print("Hello")
    else:
        form = RegistrationForm()
    return render(request, "Registration.html", {"form": form})

def userLogin(request):
    form = LoginForm(request.POST)
    if request.method == 'POST':
            username = request.POST.get('email')
            password = request.POST.get('password')
            
            #dbpwd = mydb.users.find_one({"Email": userName}, {"Password": 1, "_id": 0})
            #dbemail = mydb.users.find_one({"Email": userName})
            #adminpwd = mydb.Admins.find_one({"userName": userName}, {"password": 1, "_id": 0})
            #adminName = mydb.Admins.find_one({"userName": userName})
            
            #username = User.objects.get(userEmail=userName).userEmail
            #userPassword = User.objects.get(userPassword=password).userPassword
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "Dashboard.html")
            else:
                print(username, password)
                messages.error(request, "Username or password is incorrect")
                return render(request, "Login.html", {"form": form})
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
            