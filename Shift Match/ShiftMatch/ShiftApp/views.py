from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseForbidden, HttpResponseRedirect
import pymongo
from django.core.mail import send_mail
from .models import User, Shifts, Conversation
from .forms import RegistrationForm, LoginForm, AdminLogin, IDRequest, MatchingShiftsForm, AddShiftForm
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
import schedule
import time
from schedule import repeat, every
import pusher
from pusher import Pusher
from .pusher import pusher_client
from django.views.decorators.csrf import csrf_exempt


myclient = pymongo.MongoClient("mongodb+srv://user01:WAX5VkFPgLmrclRt@shiftmatch.mux73es.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["ShiftMatch"]
mycol = mydb["users"]


def registration(request):
    
    if request.method == 'POST':
        form1 = RegistrationForm(request.POST)
        if form1.is_valid():
            
            firstName = form1.cleaned_data['firstName']
            lastName = form1.cleaned_data['lastName']
            userEmail = form1.cleaned_data['email']
            employeeId = form1.cleaned_data['id']
            company = form1.cleaned_data['company']
            userPassword = form1.cleaned_data['password']
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
        form1 = RegistrationForm()
    return render(request, "Login-Registration.html", {"form1": form1})

def userLogin(request):
    
    if request.method == 'POST':
        form2 = LoginForm(request.POST)
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
            return render(request, "Login-Registration.html", {"form2": form2})
    else:
        form2 = LoginForm()
    return render(request, "Login-Registration.html", {"form2": form2})

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
    #upcomingShifts = Shifts.objects.filter(username=request.user.username).filter(shiftStart__gte=today).filter(ShiftPool=False).order_by('shiftStart')
    userShiftsInPool = Shifts.objects.filter(username=request.user.username).filter(ShiftPool=True)
    
    username = request.user.username
    all_events = Shifts.objects.filter(username = username)
    event_arr = []
    for i in all_events:
        event_sub_arr = {}
        shiftStart = datetime.strptime(str(i.shiftStart), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S%z")
        shiftEnd = datetime.strptime(str(i.shiftEnd), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S%z")
        hours = "Hours:",str(i.hours)
        location = "Location:",i.location
        role = "Roles:",i.qualification
        description = []
        des = hours,location,role
        description.extend(des)
        event_sub_arr['title'] = "Shift"
        event_sub_arr['start'] = shiftStart
        event_sub_arr['end'] = shiftEnd
        event_sub_arr['description'] = description
        event_arr.append(event_sub_arr)
    dataset = json.dumps(event_arr)
    
    
    context = {
        "name": name,
        "shiftsInPool": shiftsInPool,
        "upcomingShifts": dataset,
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
        hours = "Hours:",str(i.hours)
        location = "Location:",i.location
        role = "Roles:",i.qualification
        description = []
        des = hours,location,role
        description.extend(des)
        event_sub_arr['title'] = "Shift"
        event_sub_arr['start'] = shiftStart
        event_sub_arr['end'] = shiftEnd
        event_sub_arr['description'] = description
        event_arr.append(event_sub_arr)
    # data = JsonResponse((event_arr), safe=False)
    dataset = json.dumps(event_arr)
    print (dataset)
    context = {
        "shifts": dataset,
    }
                    
    return render(request, "Calendar.html", context)   

@login_required
def shiftMatching(request):
    form = MatchingShiftsForm(request.POST or None, username = request.user.username)
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


def MatchingShiftsSearch(username, shift, daysAvailabletoWork, locationNotWillingToWork, roles):
    matchingShifts = Shifts.objects.exclude(username=username).filter(shiftStart__contains=daysAvailabletoWork).exclude(qualification__contains=locationNotWillingToWork).filter(dateAvailable__contains=shift).filter(ShiftPool=True)
    print("Trying to match Shifts")
    return matchingShifts

@login_required
def MatchView(request):
    form = MatchingShiftsForm()
    daysAvailabletoWork = ""
    shift = ""
    locationNotWillingToWork = ""
    matchingShifts = ""
    username = request.user.username
    roles = request.user.qualifications
    if request.method == 'POST':
        if 'form1' in request.POST:
            shift = request.POST.get("shift")
            daysAvailabletoWork = request.POST.get("daysAvailabletoWork") 
            locationNotWillingToWork = request.POST.getlist("locations[]") 
            #Updating DB to pool and match shifts
            Shifts.objects.filter(shiftStart__contains=shift).filter(username=username).update(Matching=True)
            Shifts.objects.filter(shiftStart__contains=shift).filter(username=username).update(dateAvailable=daysAvailabletoWork)
            Shifts.objects.filter(shiftStart__contains=shift).filter(username=username).update(locationNotWillingToWork=locationNotWillingToWork)
            #Shifts.objects.filter(shiftStart__contains=shift).filter(username=username).update(ShiftPool=True)
            matchingShifts = MatchingShiftsSearch(username=username, shift=shift, daysAvailabletoWork=daysAvailabletoWork, locationNotWillingToWork=locationNotWillingToWork, roles=roles)
        if 'form2' in request.POST:
            shift = request.POST.get("shift")
            Shifts.objects.filter(id=shift).update(ShiftPool=True)
        if 'form3' in request.POST:
            shift = request.POST.get("shift")
            Shifts.objects.filter(id=shift).update(ShiftPool=False)
    else:
        form = MatchingShiftsForm()
    
    print(matchingShifts)
    if (not matchingShifts):
        print ("No Match Found!")  
        schedule.every(5).seconds.do(MatchingShiftsSearch, username, shift, daysAvailabletoWork, locationNotWillingToWork, roles)
    else:
        print(shift, matchingShifts)
        print ("Match Found!")
        #send both users emails
        
    locations = ["INBND RNR", "LAVS", "CSA", "LSA", "FEULLING", "DEICE"]
    userShiftsInMatching = Shifts.objects.filter(username=username).filter(Matching=True).filter(ShiftPool=False)
    userMatchandPool = Shifts.objects.filter(username=username).filter(Matching=True).filter(ShiftPool=True)
    context = {
        "form": form,
        "matchingShifts": matchingShifts,
        "locations": locations,
        "userMatchingShifts": userShiftsInMatching,
        "userMatchingAndPool": userMatchandPool,
        "form2": True,
        "form3": True
    }
        
    return render(request, "Match.html",context)
    
@login_required
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

@login_required
def ShiftStatusView(request):
        return render(request, "ShiftStatus.html")

@login_required
def SettingsView(request):
    
    if request.method == 'POST':
        role = request.POST.getlist("locations[]")
        User.objects.filter(username=request.user.username).update(qualifications=role)
    
    firstName = request.user.firstName
    lastName = request.user.lastName
    email = request.user.username
    password = request.user.password
    roles = request.user.qualifications
    
    locations = ["INBND RNR", "LAVS", "CSA", "LSA", "FEULLING", "DEICE"]
    
    context = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "roles": roles,
        "locations": locations
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
            location = form.cleaned_data['location']
            shift = Shifts.objects.create(shiftStart=shiftStart, shiftEnd=shiftEnd, location=location, username=request.user)
            shift.save()
            return HttpResponse(status=204)
    else:
        form = AddShiftForm()
        
    locations = ["BAGROOM", "INBND RNR", "LAVS", "CSA", "LSA", "FEULLING", "DEICE", "RT"]
    
    context = {
        "form": form,
        "locations": locations
    }
         
    return render(request, "Add_Shift.html", context)


def Chatview(request):
    userTwo = ''
    user2 = ''
    channel = ''
    sortedIds = ''
    if request.method == 'POST':
        userTwo = request.POST.get('user')
        if userTwo == 'Group':
            channel = 'my_channel'
            #conversations(request, channel)
        else:
            user2 = User.objects.get(firstName=userTwo)
            sortedIds = sorted([request.user.id, user2.id])
            channel = '-'.join(map(str, sortedIds))
            #conversations(request, channel)
    users = User.objects.exclude(username=request.user.username)
    context = {
        "users": users,
        "currentUser": request.user,
        "userTwo": user2,
        "channel": channel,
        "firstName": userTwo
    }
    
    return render(request, "Chat.html", context)

pusher = Pusher(app_id=u'1781407', key=u'4b5bb58a37e41d8eb66d', secret=u'4be0810d178aa1aa094c', cluster=u'us3')

@csrf_exempt
def broadcast(request):
    channel = ''
    if request.method == 'POST':
        channel = request.POST.get('channel', '')
    print(channel)
    # collect the message from the post parameters, and save to the database
    message = Conversation(message=request.POST.get('message', ''), status='', user=request.user, channel=channel)
    message.save()
    # create an dictionary from the message instance so we can send only required details to pusher
    message = {'name': message.user.firstName, 'status': message.status, 'message': message.message, 'id': message.id}
    #trigger the message, channel and event to pusher
    pusher.trigger(channel, u'an_event', message)
    # return a json response of the broadcasted message
    return JsonResponse(message, safe=False)

def conversations(request):
    channel = ''
    if request.method == 'GET':
        channel = request.GET.get('channel', '')
    data = Conversation.objects.all().filter(channel=channel)
    data = [{'name': person.user.firstName, 'status': person.status, 'message': person.message, 'id': person.id} for person in data]
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def delivered(request, id):
    message = Conversation.objects.get(pk=id)
    # verify it is not the same user who sent the message that wants to trigger a delivered event
    if request.user.id != message.user.id:
        socket_id = request.POST.get('socket_id', '')
        message.status = 'Delivered'
        message.save()
        message = {'name': message.user.firstName, 'status': message.status, 'message': message.message, 'id': message.id}
        pusher.trigger(u'my_channel', u'delivered_message', message, socket_id)
        return HttpResponse('ok')
    else:
        return HttpResponse('Awaiting Delivery')
    
def pusher_auth(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    
    pusher_client

    # We must generate the token with pusher's service
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id']
    )
        
    return JsonResponse(payload)

