from django.contrib import admin
from userauth.models import Request, Accepted_req, Completed_trip


# Register your models here.
admin.site.register(Request)
admin.site.register(Accepted_req)
admin.site.register(Completed_trip)