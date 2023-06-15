from django.db import models
from django.contrib.auth.hashers import make_password
from pygeodesic import geodesic
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Request(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_id = request_id = models.BigAutoField(primary_key=True)
    patient = models.CharField(max_length=20)
    pick_latitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    pick_longitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    contact = models.CharField(max_length=10)
    hospital_latitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    hospital_longitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    request_time = models.DateTimeField(default=timezone.now)
    assigned = models.BooleanField(default=False)
     
    def __str__(self):
         return f"Request #{self.request_id}"
    
    def calculate_distance(self):
        if self.pick_latitude is None or self.pick_longitude is None or \
                self.hospital_latitude is None or self.hospital_longitude is None:
            return None
        pickup = (float(self.pick_latitude), float(self.pick_longitude))
        dropoff = (float(self.hospital_latitude), float(self.hospital_longitude))
        distance = geodesic(pickup, dropoff).kilometers
        return distance
    
    

class Accepted_req(models.Model):

    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    pending_id = models.BigAutoField(primary_key=True)


    def __str__(self):
        return f"PendingReq - Driver: {self.driver.username}, Request: {self.request}"

    def calculate_distance(self):
        pickup_latitude = self.request.pick_latitude
        pickup_longitude = self.request.pick_longitude
        hospital_latitude = self.request.hospital_latitude
        hospital_longitude = self.request.hospital_longitude

        if (
            pickup_latitude is None
            or pickup_longitude is None
            or hospital_latitude is None
            or hospital_longitude is None
        ):
            return None

        pickup = (float(pickup_latitude), float(pickup_longitude))
        dropoff = (float(hospital_latitude), float(hospital_longitude))
        distance = geodesic(pickup, dropoff).kilometers
        return distance

class Completed_trip(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    # Other fields related to the completed trip

    def __str__(self):
        return f"Completed Trip - Driver: {self.driver.username}, Request: {self.request}"






    



