from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ParkingLot)
admin.site.register(Slot)
admin.site.register(Ticket)
admin.site.register(UploadPrimaryData)