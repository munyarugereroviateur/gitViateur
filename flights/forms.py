from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Airplane, Flight, Passenger, Ticket

W = {'class': 'form-control'}
S = {'class': 'form-select'}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs=W))
    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs=W)}


class AirplaneForm(forms.ModelForm):
    class Meta:
        model  = Airplane
        fields = ['airplane_code', 'model', 'manufacturer',
                  'capacity', 'registration_number', 'status']
        widgets = {
            'airplane_code':       forms.TextInput(attrs=W),
            'model':               forms.TextInput(attrs=W),
            'manufacturer':        forms.TextInput(attrs=W),
            'capacity':            forms.NumberInput(attrs=W),
            'registration_number': forms.TextInput(attrs=W),
            'status':              forms.Select(attrs=S),
        }


class FlightForm(forms.ModelForm):
    class Meta:
        model  = Flight
        fields = ['flight_number', 'airplane', 'origin', 'destination',
                  'departure_time', 'arrival_time', 'flight_date',
                  'status', 'gate_number']
        widgets = {
            'flight_number':  forms.TextInput(attrs=W),
            'airplane':       forms.Select(attrs=S),
            'origin':         forms.TextInput(attrs=W),
            'destination':    forms.TextInput(attrs=W),
            'departure_time': forms.DateTimeInput(
                attrs={**W, 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'),
            'arrival_time':   forms.DateTimeInput(
                attrs={**W, 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'),
            'flight_date':    forms.DateInput(
                attrs={**W, 'type': 'date'}),
            'status':         forms.Select(attrs=S),
            'gate_number':    forms.TextInput(attrs=W),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['arrival_time'].input_formats   = ['%Y-%m-%dT%H:%M']


class PassengerForm(forms.ModelForm):
    class Meta:
        model  = Passenger
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth',
                  'passport_number', 'nationality', 'phone', 'email',
                  'passport_photo', 'address']
        widgets = {
            'first_name':      forms.TextInput(attrs=W),
            'last_name':       forms.TextInput(attrs=W),
            'gender':          forms.Select(attrs=S),
            'date_of_birth':   forms.DateInput(attrs={**W, 'type': 'date'}),
            'passport_number': forms.TextInput(attrs=W),
            'nationality':     forms.TextInput(attrs=W),
            'phone':           forms.TextInput(attrs=W),
            'email':           forms.EmailInput(attrs=W),
            'address':         forms.Textarea(attrs={**W, 'rows': 3}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = ['passenger', 'flight', 'seat_number',
                  'ticket_class', 'price']
        widgets = {
            'passenger':    forms.Select(attrs=S),
            'flight':       forms.Select(attrs=S),
            'seat_number':  forms.TextInput(attrs={**W, 'placeholder': 'e.g. 14A'}),
            'ticket_class': forms.Select(attrs=S),
            'price':        forms.NumberInput(attrs=W),
        }


class CheckInForm(forms.ModelForm):
    class Meta:
        model  = Ticket
        fields = ['seat_number']
        widgets = {
            'seat_number': forms.TextInput(
                attrs={**W, 'placeholder': 'e.g. 12B'})
        }


class FlightSearchForm(forms.Form):
    origin = forms.CharField(required=False,
        widget=forms.TextInput(attrs={
            **W, 'placeholder': 'Origin city e.g. Kigali'}))
    destination = forms.CharField(required=False,
        widget=forms.TextInput(attrs={
            **W, 'placeholder': 'Destination e.g. Nairobi'}))