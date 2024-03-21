from django.shortcuts import render, redirect
import pymongo
from django.core.mail import send_mail
from .models import User, Shifts
from .forms import RegistrationForm, LoginForm, AdminLogin, IDRequest, ShiftPoolForm
from django.contrib import messages
from .settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required

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
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
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
        
@login_required
def dashboard(request):
    return render(request, "Dashboard.html")
        
@login_required
def calendarShiftInput(request):
    username = request.user.username
    all_events = Shifts.objects.filter(username = username)
    event_arr = []
    for i in all_events:
        event_sub_arr = {}
        shiftStart = datetime.strptime(str(i.shiftStart), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S%z")
        shiftEnd = datetime.strptime(str(i.shiftEnd), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S%z")
        hours = str(i.hours)
        event_sub_arr['title'] = "Shift"
        event_sub_arr['start'] = shiftStart
        event_sub_arr['end'] = shiftEnd
        event_arr.append(event_sub_arr)
    # data = JsonResponse((event_arr), safe=False)
    dataset = json.dumps(event_arr)
    print (dataset)
    context = {
        "shifts": dataset
    }
                    
    return render(request, "Calendar.html", context)   

@login_required
def shiftMatching(request):
    form = ShiftPoolForm(request.POST or None, username = request.user.username)
    username = request.user.username
    if request.method == 'POST':
        shift = request.POST.get("shift")
        daysAvailabletoWork = request.POST.get("daysAvailabletoWork")
        print(shift)
        Shifts.objects.filter(username=username).filter(shiftStart__contains=shift).update(ShiftPool=True)
        
    shiftAvailable = Shifts.objects.filter(ShiftPool = True).filter(dateAvailable = daysAvailabletoWork)
        
    return render(request, "ShiftPool.html", {"shifts": shiftAvailable, "form": form})

def calendarView(request):
    
    
        return render(request, "Calendar.html")

def TradePoolView(request):
    shiftsAvaible = Shifts.objects.filter(ShiftPool = True)
    if request.method == 'POST':
        free = request.POST.get("free")
        paid = request.POST.get("paid")
        
        if free == True:
            shiftsAvaible = Shifts.objects.filter(ShiftPool = True).filter(isPaid = False)
        if paid == True:
            shiftsAvaible = Shifts.objects.filter(ShiftPool = True).filter(isPaid = True)
    
    return render(request, "TradePool.html", {"shifts": shiftsAvaible})

def PickupPoolView(request):
    form = ShiftPoolForm(request.POST or None, username = request.user.username, use_required_attribute = False)
    daysAvailabletoWork = "Hello"
    shift = "Hello"
    username = request.user.username
    if request.method == 'POST':
        shift = request.POST.get("shift")
        daysAvailabletoWork = request.POST.get("daysAvailabletoWork")
        if request.POST.get("post_shift"):
            Shifts.objects.filter(username=username).filter(shiftStart__contains=shift).update(ShiftPool=True)
            Shifts.objects.filter(username=username).filter(shiftStart__contains=shift).update(dateAvailable=daysAvailabletoWork)
        elif request.POST.get("shift_match"):
            Shifts.objects.filter(username=username).filter(shiftStart__contains=shift).filter(ShiftPool=False).update(dateAvailable=daysAvailabletoWork)  
    shiftAvailable = Shifts.objects.filter(ShiftPool=True).filter(dateAvailable__contains=shift)
        
    return render(request, "PickupPool.html", {"shifts": shiftAvailable, "form": form})

def pickingUpShifts(request):
    username = request.user.username
    if request.method == 'POST':
        shift = request.POST.get("shift")
        print (shift)
        Shifts.objects.filter(id=shift).update(username = username)
        Shifts.objects.filter(id=shift).update(ShiftPool=False)
    shiftsAvailable = Shifts.objects.filter(ShiftPool=True)
    return render(request, "TradePool.html", {"shifts": shiftsAvailable})