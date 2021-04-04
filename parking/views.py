from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import ParkingLot, Ticket, Slot

# Create your views here.
class ParkingLotList(ListView):
    model = ParkingLot
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parking_list = ParkingLot.objects.all().order_by('modified_at')
        context['parking_list'] = parking_list
        return context


class SlotList(ListView):
    model = Slot
    paginate_by = 10
    template_name = 'parking/slot_list.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['slot_list'] = Slot.objects.all().order_by('modified_at')
        return context

class TicketList(ListView):
    model = Ticket
    paginate_by= 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_list'] = Ticket.objects.all().order_by('modified_at')
        return context