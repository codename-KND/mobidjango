from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse,HttpResponse
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .userSer import mobiUser,RequestSerializer, AcceptedRequestSerializer,MpesaSerializer
from django.contrib.auth.models import Group
from rest_framework.exceptions import NotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from pygeodesic import geodesic
from .models import User, Request, Accepted_req, Completed_trip
from django_daraja.mpesa.core import MpesaClient
from django.shortcuts import get_object_or_404

##Create youur views here.
@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    userinfo = {
        "id" : user.id,
        'username': user.username,
        'email': user.email     
    }


    return Response({'user_info': userinfo,'token': token})

#userlogin end  
@api_view(['POST'])
def register(request):
    serializer = mobiUser(data= request.data)
    serializer.is_valid(raise_exception= True)
    user = serializer.save()
    group_name = "generalUser"
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
    except Group.DoesNotExist:
         raise NotFound("The specified group does not exist.")
    
    _, token = AuthToken.objects.create(user)
    userinfo = {
    "id" : user.id,
    'username': user.username,
    'email': user.email}

    return Response({'user_info': userinfo,'token': token})

#driver login endpoint
@api_view(['POST'])
def driverRegister(request):
    serializer = mobiUser(data= request.data)
    serializer.is_valid(raise_exception= True)
    user = serializer.save()

    group_name = "driverUser"
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        
    except Group.DoesNotExist:
         raise NotFound("The specified group does not exist.")
    
    _, token = AuthToken.objects.create(user)
    userinfo = {
    "id" : user.id,
    'username': user.username,
    'email': user.email}

    return Response({'user_info': userinfo,'token': token})

#user request creation endpoint 
@api_view(['POST'])
@login_required
@csrf_exempt
def user_request(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        serializer.save(user=user, request_time=timezone.now())

        #distance = serializer.instance.calculate_distance()
        response_data = {
            'request_id': serializer.instance.request_id,
            'patient': serializer.instance.patient,
            #'distance': distance
        }

        return Response(response_data)
    return Response(serializer.errors, status=400)

## driver retrieves and view all requests endpoint
@api_view(['GET'])
@login_required
def available_requests(request):
    requests = Request.objects.filter(assigned=False)
    # create filter(user=request.user) for user

    serializer = RequestSerializer(requests, many=True)

    response_data = serializer.data

    return Response(response_data)


##driver 
@api_view(['GET'])
@login_required
def request_detail(request, request_id):
    try:
    
        request_obj = Request.objects.get(request_id=request_id)# add this filter user=request.user)
    except Request.DoesNotExist:
        return Response({'error': 'Requests not found'}, status=404)

    serializer = RequestSerializer(request_obj)
    response_data = serializer.data

    return Response(response_data)


@api_view(['POST'])
@login_required
def accepted_requests(request):

    request_id = request.data.get('request_id')
    

    try:
        request_obj = Request.objects.get(pk=request_id)
        driver_obj = request.user

        accepted_request = Accepted_req(driver=driver_obj, request=request_obj, status=True)
        accepted_request.save()

        request_obj.assigned = True
        request_obj.save()
        serializer = AcceptedRequestSerializer(accepted_request)

        response_data = serializer.data

        return Response(response_data)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)
    except User.DoesNotExist:
        return Response({'error': 'Driver not found'}, status=404)

@api_view(['POST'])
#@login_required
def complete_trip(request):
    accepted_request_id = request.data.get('pending_id')

    accepted_request = get_object_or_404(Accepted_req, pending_id=accepted_request_id)
    request_instance = accepted_request.request
    contact = request_instance.contact

    try:
        accepted_request = Accepted_req.objects.get(pk=accepted_request_id)
        completed_trip = Completed_trip(
            request=accepted_request.request,
            driver=accepted_request.driver,
            #distance=accepted_request.request.calculate_distance(),
        )
        completed_trip.save()
        accepted_request.status = False
        client = MpesaClient()
        phone_number = contact
        amount=1
        account_refrence=' MOBILANCE'
        transaction_desc = 'TRIP PAYMENT'
        callback_url = 'http://api.darajambili.com/express-payment'
        client.stk_push(phone_number,amount,account_refrence,transaction_desc,callback_url)
    
        accepted_request.save()
        return Response({'message': 'Trip completed successfully'})
    except Accepted_req.DoesNotExist:
        return Response({'error': 'Accepted request not found'}, status=404)

@api_view(['GET'])
@login_required
def my_trips(request):
    user = request.user

    # Retrieve completed trips for the user
    completed_trips = Completed_trip.objects.filter(request__user=user)

    # Prepare the data to be returned
    data = []
    for trip in completed_trips:
        trip_data = {
            'driver': trip.driver.username,
            'requestId': trip.request.request_id,
            "patientName": trip.request.patient,
            "hospitalLatitude": trip.request.hospitalLatitude,
            "hospitalLongitude":trip.request.hospitalLongitude
        }
        data.append(trip_data)

    return JsonResponse(data, safe=False)

@api_view(['POST']) 

def payment(request):

    pending_id = request.data.get('pending_id')
    accepted_request = get_object_or_404(Accepted_req, pending_id=pending_id)
    request_instance = accepted_request.request
    contact = request_instance.contact

    client = MpesaClient()
    phone_number = '0712501695'
    amount=1
    account_refrence=' MOBILANCE'
    transaction_desc = 'TRIP PAYMENT'
    # callback_url = ' http://127.0.0.1:4040'
    callback_url = 'https://c20a-41-90-69-56.ngrok-free.app/api/payment-result'

    server_response = client.stk_push(phone_number,amount,account_refrence,transaction_desc,callback_url)
    #response = MpesaSerializer(server_response)
    
    return HttpResponse(server_response)

@csrf_exempt
def payment_results(self, request):
    cl = MpesaClient()
    if request.method == 'POST':
        result = cl.parse_stk_result(request.body)
        print(result)

@api_view(['GET'])
@login_required
def drivertrips(request):
    user = request.user

    # Retrieve completed trips for the user
    completed_trips = Completed_trip.objects.filter(driver_id=user)

    # Prepare the data to be returned
    data = []
    for trip in completed_trips:
        trip_data = {
            
            'requestId': trip.request.request_id,
            "patientName": trip.request.patient,
            "hospitalLatitude": trip.request.hospitalLatitude,
            "hospitalLongitude":trip.request.hospitalLongitude
        }
        data.append(trip_data)

    return JsonResponse(data, safe=False)
