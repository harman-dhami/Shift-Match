"""
URL configuration for ShiftMatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  frohttps://www.w3schools.com/howto/howto_css_switch.aspm other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import registration, userLogin, adminLogin, idRequest, calendarShiftInput, shiftMatching, calendarView, TradePoolView, PickupPoolView, dashboard, pickingUpShifts

urlpatterns = [
    path('', registration, name='registration'),
    path('ShiftApp/', userLogin, name='userLogin'),
    path('ShiftApp/adminLogin', adminLogin, name='adminLogin'),
    path('ShiftApp/idRequest', idRequest, name='idRequest'),
    path('ShiftApp/calendarShiftInput', calendarShiftInput, name='calendarShiftInput'),
    path('ShiftApp/shiftMatching', shiftMatching, name='shiftMatching'),
    path('ShiftApp/calendarView', calendarView, name='calendarView'),
    path('ShiftApp/MatchView', MatchView, name='MatchView'),
    path('ShiftApp/PickupPoolView', PickupPoolView, name='PickupPoolView'),
    path('ShiftApp/dashboard', dashboard, name='dashboard'),
    path('ShiftApp/pickingUpShifts', pickingUpShifts, name='pickingUpShifts')
]