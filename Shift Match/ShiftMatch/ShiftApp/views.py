from django.shortcuts import render, redirect, HttpResponse
import pymongo
from django.core.mail import send_mail
from .models import User, Shifts
from .forms import RegistrationForm, LoginForm, AdminLogin, IDRequest, ShiftPoolForm, AddShiftForm
from django.contrib import messages
from .settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
import json
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Q


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
    name = request.user.firstName
    
    today = now().date()
    shiftsInPool = Shifts.objects.exclude(username=request.user.username).filter(ShiftPool=True).filter(shiftStart__gte=today).order_by('shiftStart')
    upcomingShifts = Shifts.objects.filter(username=request.user.username).filter(shiftStart__gte=today).filter(ShiftPool=False).order_by('shiftStart')
    userShiftsInPool = Shifts.objects.filter(username=request.user.username).filter(ShiftPool=True)
    
    context = {
        "name": name,
        "shiftsInPool": shiftsInPool,
        "upcomingShifts": upcomingShifts,
        "userShiftsInPool": userShiftsInPool
    }
    return render(request, "Dashboard.html", context)
        
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
        
        shiftUpdate = Shifts.objects.filter(shiftStart=shift).update(ShiftPool=True)
        
    shiftAvailable = Shifts.objects.filter(ShiftPool = True).filter(dateAvailable = daysAvailabletoWork)
        
    return render(request, "ShiftPool.html", {"shifts": shiftAvailable, "form": form})

def calendarView(request):
        

        return render(request, "Calendar.html")

def PickupPoolView(request):
    
    paidShifts = Shifts.objects.filter(isPaid=True).filter(ShiftPool=True)
    notPaid = Shifts.objects.filter(isPaid=False).filter(ShiftPool=True)
    
    context = {
        "paid": paidShifts,
        "notPaid": notPaid
    }
    
    return render(request, "PickupPool.html", context)

def MatchView(request):
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
    #send email using django email service; setup testing email using django framework
    return render(request, "Match.html", {"shifts": shiftsAvailable})

def ShiftStatusView(request):
        return render(request, "ShiftStatus.html")

def SettingsView(request):
    
    if request.method == 'POST':
        role = request.POST.get("role")
        
        User.objects.filter(username=request.user.username).update(qualifications=role)
    
    firstName = request.user.firstName
    lastName = request.user.lastName
    email = request.user.username
    password = request.user.password
    roles = request.user.qualifications
    
    context = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "roles": roles
    }
    return render(request, "Settings.html", context)

def userLogout(request):
    logout(request)
    return redirect('userLogin')

def addShift(request):
    if request.method == 'POST':
        form=AddShiftForm(request.POST)
        if form.is_valid():
            shiftStart = form.cleaned_data['shiftStart']
            shiftEnd = form.cleaned_data['shiftEnd']
            hours = form.cleaned_data['hours']
            shift = Shifts.objects.create(shiftStart=shiftStart, shiftEnd=shiftEnd, hours=hours, username=request.user)
            shift.save()
            return HttpResponse(status=204)
    else:
        form = AddShiftForm()
         
    
    return render(request, "Add_Shift.html", {"form": form})