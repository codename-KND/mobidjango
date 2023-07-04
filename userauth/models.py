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
    pickLatitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    pickLongitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    contact = models.CharField(max_length=10)
    hospitalLatitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    hospitalLongitude = models.DecimalField(max_digits=22,decimal_places=16, blank=True,null=True)
    request_time = models.DateTimeField(default=timezone.now)
    assigned = models.BooleanField(default=False)
     
    def __str__(self):
         return f"Request #{self.request_id}"
    
    # def calculate_distance(self):
    #     if self.pick_latitude is None or self.pick_longitude is None or \
    #             self.hospital_latitude is None or self.hospital_longitude is None:
    #         return None
    #     pickup = (float(self.pick_latitude), float(self.pick_longitude))
    #     dropoff = (float(self.hospital_latitude), float(self.hospital_longitude))
    #     distance = geodesic(pickup, dropoff).kilometers
    #     return distance
    
    

class Accepted_req(models.Model):

    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    pending_id = models.BigAutoField(primary_key=True)


    def __str__(self):
        return f"PendingReq - Driver: {self.driver.username}, Request: {self.request}"

    def calculate_distance(self):
        pickupLatitude = self.request.pickLatitude
        pickupLongitude = self.request.pickLongitude
        hospitalLatitude = self.request.hospitalLatitude
        hospitalLongitude = self.request.hospitalLongitude

        if (
            pickupLatitude is None
            or pickupLongitude is None
            or hospitalLatitude is None
            or hospitalLongitude is None
        ):
            return None

        pickup = (float(pickupLatitude), float(pickupLongitude))
        dropoff = (float(hospitalLatitude), float(hospitalLongitude))
        distance = geodesic(pickup, dropoff).kilometers
        return distance

class Completed_trip(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    

    def __str__(self):
        return f"Completed Trip - Driver: {self.driver.username}, Request: {self.request}"






    



