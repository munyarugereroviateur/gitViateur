from rest_framework import serializers
from .models import Airplane, Flight, Passenger, Ticket


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Airplane
        fields = ['id', 'airplane_code', 'model', 'manufacturer',
                  'capacity', 'registration_number', 'status']


class FlightSerializer(serializers.ModelSerializer):
    airplane_detail = AirplaneSerializer(source='airplane', read_only=True)
    airplane = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(), write_only=True)

    class Meta:
        model  = Flight
        fields = ['id', 'flight_number', 'origin', 'destination',
                  'departure_time', 'arrival_time', 'flight_date',
                  'status', 'gate_number', 'airplane', 'airplane_detail']


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Passenger
        fields = ['id', 'first_name', 'last_name', 'passport_number',
                  'nationality', 'email', 'phone']


class TicketSerializer(serializers.ModelSerializer):
    passenger_detail = PassengerSerializer(source='passenger', read_only=True)
    flight_detail    = FlightSerializer(source='flight', read_only=True)

    class Meta:
        model  = Ticket
        fields = ['id', 'ticket_number', 'seat_number', 'ticket_class',
                  'price', 'check_in_status', 'boarding_status',
                  'ticket_status', 'booking_date', 'passenger', 'flight',
                  'passenger_detail', 'flight_detail']