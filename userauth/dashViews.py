from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Request, Accepted_req, Completed_trip
from .Dashinfo import DashinfoClass
from .userSer import RequestSerializer
from datetime import datetime, timedelta


def index(request):
    #get and populate dashboard with data
    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    info ={
        'drivercount': dashinfo['drivercount'],
        'tripcount':dashinfo['tripcount'],
        'progresscount':dashinfo['progresscount'],
        }
    return render(request, 'base.html',{'info':info})

def drivers_list(request):
    drivers = User.objects.filter(groups__name='driverUser')
    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    info = {
        'drivers': drivers,
        'drivercount': dashinfo['drivercount'],
        'tripcount':dashinfo['tripcount'],
        'progresscount':dashinfo['progresscount'],
    }
    return render(request, 'drivers.html', {'info': info})


def customer_list(request):

    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    customer = User.objects.filter(groups__name='generalUser')
    info = {
        'drivercount': dashinfo['drivercount'],
        'tripcount':dashinfo['tripcount'],
        'progresscount':dashinfo['progresscount'],
        'customer': customer,
        
    }

    return render(request, 'admin-dashboard/generalUser.html',{'info': info} )



def request_list(request):
    
    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    requests = Request.objects.filter(assigned=False)
    
    info ={
        'drivercount': dashinfo['drivercount'],
        'tripcount':dashinfo['tripcount'],
        'progresscount':dashinfo['progresscount'],
        'requests': [{'request': req, 'user': req.user, 'time': req.request_time} for req in requests],
    }
    print(requests)
    

    return render(request, 'admin-dashboard/requests.html',{'info': info})
    

def trips_list(request):

    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    current_trips = Accepted_req.objects.filter(status= True)
    info ={
        'drivercount': dashinfo['drivercount'],
        'tripcount':dashinfo['tripcount'],
        'progresscount':dashinfo['progresscount'],
        'currentTrip': [{'driver': trip.driver.username, 'patient': trip.request.patient} for trip in current_trips],
    }
     
    print(current_trips)
    return render(request, 'admin-dashboard/tripProgress.html',{'info': info})

def completed_trip(request):
    dashinfo = DashinfoClass()
    dashinfo.populate_info()
    complete_trip = Completed_trip.objects.all()
    selected_date = request.GET.get('date')
    print(selected_date)

    if selected_date == 'alltime':
        pass
    else:
        today = datetime.now().date()
        if selected_date == 'today':
            start_date = today
            end_date = start_date + timedelta(days=1)
        elif selected_date == 'lastweek':
            start_date = today - timedelta(days=7)
            end_date = today
        elif selected_date == 'lastmonth':
            start_date = today - timedelta(days=30)
            end_date = today
        elif selected_date == 'lastyear':
            start_date = today - timedelta(days=365)
            end_date = today
        else:
            start_date = None
            end_date = None

        if start_date and end_date:
            complete_trip = complete_trip.filter(request__request_time__gte=start_date,
                                                  request__request_time__lt=end_date + timedelta(days=1))

    info ={
        'drivercount': dashinfo['drivercount'],
        'tripcount': dashinfo['tripcount'],
        'progresscount': dashinfo['progresscount'],
        'currentTrip': [{'driver': trip.driver.username,
                          'patient': trip.request.patient,
                          'date': trip.request.request_time,
                          'distance': trip.distance} for trip in complete_trip],
    }
    return render(request, 'admin-dashboard/completedtrips.html', {'info': info})