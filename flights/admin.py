from django.contrib import admin
from .models import Airplane, Flight, Passenger, Ticket


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display  = ['airplane_code', 'model', 'manufacturer',
                     'capacity', 'registration_number', 'status']
    list_filter   = ['status', 'manufacturer']
    search_fields = ['airplane_code', 'registration_number', 'model']


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display  = ['flight_number', 'origin', 'destination',
                     'flight_date', 'departure_time', 'status',
                     'airplane', 'gate_number']
    list_filter   = ['status', 'flight_date']
    search_fields = ['flight_number', 'origin', 'destination']


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'passport_number',
                     'nationality', 'email', 'phone']
    list_filter   = ['nationality', 'gender']
    search_fields = ['passport_number', 'last_name', 'email']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['ticket_number', 'passenger', 'flight',
                     'seat_number', 'ticket_class', 'price',
                     'check_in_status', 'boarding_status', 'ticket_status']
    list_filter   = ['ticket_status', 'ticket_class', 'check_in_status']
    search_fields = ['ticket_number', 'passenger__passport_number']