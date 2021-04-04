from django.conf.urls import url
from django.urls import path
from .views import *
app_name = 'parking'

urlpatterns = [
    path('', ParkingLotList.as_view(), name='parking_lot'),
    path('slot/', SlotList.as_view(), name='slot'),
    path('ticket/', TicketList.as_view(), name='ticket')
]