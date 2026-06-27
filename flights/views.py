from django.shortcuts               import render, get_object_or_404, redirect
from django.views.generic           import ListView, CreateView, UpdateView, DeleteView
from django.urls                    import reverse_lazy
from django.http                    import JsonResponse
from django.contrib.auth            import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.db.models               import Q
from rest_framework                 import generics
from rest_framework.decorators      import api_view, renderer_classes
from rest_framework.renderers       import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response        import Response
from .models       import Airplane, Flight, Passenger, Ticket
from .forms        import (AirplaneForm, FlightForm, PassengerForm,
                           TicketForm, CheckInForm, FlightSearchForm, RegisterForm)
from .serializers  import (FlightSerializer, TicketSerializer,
                           PassengerSerializer, AirplaneSerializer)


def home_view(request):
    context = {
        'total_airplanes':  Airplane.objects.count(),
        'total_flights':    Flight.objects.count(),
        'total_passengers': Passenger.objects.count(),
        'total_tickets':    Ticket.objects.count(),
    }
    return render(request, 'flights/home.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'flights/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AirplaneListView(ListView):
    model = Airplane
    template_name = 'flights/airplane_list.html'
    context_object_name = 'airplanes'


@method_decorator(login_required, name='dispatch')
class AirplaneCreateView(CreateView):
    model = Airplane
    form_class = AirplaneForm
    template_name = 'flights/airplane_form.html'
    success_url = reverse_lazy('airplane-list')


@method_decorator(login_required, name='dispatch')
class AirplaneUpdateView(UpdateView):
    model = Airplane
    form_class = AirplaneForm
    template_name = 'flights/airplane_form.html'
    success_url = reverse_lazy('airplane-list')


@method_decorator(login_required, name='dispatch')
class AirplaneDeleteView(DeleteView):
    model = Airplane
    template_name = 'flights/airplane_confirm_delete.html'
    success_url = reverse_lazy('airplane-list')


@method_decorator(login_required, name='dispatch')
class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'
    queryset = Flight.objects.select_related('airplane').all()


@method_decorator(login_required, name='dispatch')
class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flights/flight_form.html'
    success_url = reverse_lazy('flight-list')


@method_decorator(login_required, name='dispatch')
class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flights/flight_form.html'
    success_url = reverse_lazy('flight-list')


@method_decorator(login_required, name='dispatch')
class FlightDeleteView(DeleteView):
    model = Flight
    template_name = 'flights/flight_confirm_delete.html'
    success_url = reverse_lazy('flight-list')


@method_decorator(login_required, name='dispatch')
class PassengerListView(ListView):
    model = Passenger
    template_name = 'flights/passenger_list.html'
    context_object_name = 'passengers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Passenger.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(passport_number__icontains=q) |
                Q(nationality__icontains=q)
            )
        return queryset


@method_decorator(login_required, name='dispatch')
class PassengerCreateView(CreateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'flights/passenger_form.html'
    success_url = reverse_lazy('passenger-list')


@method_decorator(login_required, name='dispatch')
class PassengerUpdateView(UpdateView):
    model = Passenger
    form_class = PassengerForm
    template_name = 'flights/passenger_form.html'
    success_url = reverse_lazy('passenger-list')


@method_decorator(login_required, name='dispatch')
class PassengerDeleteView(DeleteView):
    model = Passenger
    template_name = 'flights/passenger_confirm_delete.html'
    success_url = reverse_lazy('passenger-list')


@method_decorator(login_required, name='dispatch')
class TicketListView(ListView):
    model = Ticket
    template_name = 'flights/ticket_list.html'
    context_object_name = 'tickets'
    queryset = Ticket.objects.select_related('flight', 'passenger').all()


@method_decorator(login_required, name='dispatch')
class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'flights/ticket_form.html'
    success_url = reverse_lazy('ticket-list')


@method_decorator(login_required, name='dispatch')
class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'flights/ticket_form.html'
    success_url = reverse_lazy('ticket-list')


@method_decorator(login_required, name='dispatch')
class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'flights/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')


@login_required
def issue_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket-list')
    else:
        form = TicketForm()
    return render(request, 'flights/issue_ticket.html', {'form': form})


@login_required
def checkin(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = CheckInForm(request.POST, instance=ticket)
        if form.is_valid():
            t = form.save(commit=False)
            t.check_in_status = True
            t.save()
            return redirect('ticket-list')
    else:
        form = CheckInForm(instance=ticket)
    return render(request, 'flights/checkin.html',
                  {'form': form, 'ticket': ticket})


@login_required
def manifest(request, pk):
    flight = get_object_or_404(
        Flight.objects.prefetch_related('tickets__passenger'), pk=pk)
    tickets = flight.tickets.all()
    return render(request, 'flights/manifest.html',
                  {'flight': flight, 'tickets': tickets})


@login_required
def flight_search(request):
    form    = FlightSearchForm(request.GET or None)
    flights = Flight.objects.none()
    if form.is_valid():
        origin      = form.cleaned_data.get('origin', '')
        destination = form.cleaned_data.get('destination', '')
        q = Q()
        if origin:
            q &= Q(origin__icontains=origin)
        if destination:
            q &= Q(destination__icontains=destination)
        flights = Flight.objects.select_related('airplane').filter(q)
    return render(request, 'flights/flight_search.html',
                  {'form': form, 'flights': flights})


# ============================================================
# FLIGHT OCCUPANCY API — with DRF Browsable Interface
# ============================================================
@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def flight_occupancy_api(request, pk):
    flight   = get_object_or_404(Flight, pk=pk)
    capacity = flight.airplane.capacity
    sold     = flight.tickets.count()
    percent  = round((sold / capacity) * 100, 2) if capacity > 0 else 0
    data = {
        'flight_number':        flight.flight_number,
        'origin':               flight.origin,
        'destination':          flight.destination,
        'flight_date':          str(flight.flight_date),
        'airplane':             str(flight.airplane),
        'total_capacity':       capacity,
        'tickets_sold':         sold,
        'occupancy_percentage': percent,
        'status': (
            'FULL'        if percent == 100 else
            'ALMOST FULL' if percent >= 80  else
            'AVAILABLE'
        )
    }
    return Response(data)


# ============================================================
# DRF LIST / CREATE ENDPOINTS
# ============================================================
class FlightListCreateAPI(generics.ListCreateAPIView):
    queryset         = Flight.objects.select_related('airplane').all()
    serializer_class = FlightSerializer


class TicketListCreateAPI(generics.ListCreateAPIView):
    queryset         = Ticket.objects.select_related('flight', 'passenger').all()
    serializer_class = TicketSerializer