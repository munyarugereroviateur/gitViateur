from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Auth
    path('accounts/register/', views.register_view, name='register'),

    # Airplane CRUD
    path('airplanes/',                  views.AirplaneListView.as_view(),   name='airplane-list'),
    path('airplanes/add/',              views.AirplaneCreateView.as_view(), name='airplane-create'),
    path('airplanes/<int:pk>/edit/',    views.AirplaneUpdateView.as_view(), name='airplane-update'),
    path('airplanes/<int:pk>/delete/',  views.AirplaneDeleteView.as_view(), name='airplane-delete'),

    # Flight CRUD
    path('flights/',                    views.FlightListView.as_view(),     name='flight-list'),
    path('flights/add/',                views.FlightCreateView.as_view(),   name='flight-create'),
    path('flights/<int:pk>/edit/',      views.FlightUpdateView.as_view(),   name='flight-update'),
    path('flights/<int:pk>/delete/',    views.FlightDeleteView.as_view(),   name='flight-delete'),

    # Passenger CRUD
    path('passengers/',                 views.PassengerListView.as_view(),   name='passenger-list'),
    path('passengers/add/',             views.PassengerCreateView.as_view(), name='passenger-create'),
    path('passengers/<int:pk>/edit/',   views.PassengerUpdateView.as_view(), name='passenger-update'),
    path('passengers/<int:pk>/delete/', views.PassengerDeleteView.as_view(), name='passenger-delete'),

    # Ticket CRUD
    path('tickets/',                    views.TicketListView.as_view(),      name='ticket-list'),
    path('tickets/add/',                views.TicketCreateView.as_view(),    name='ticket-create'),
    path('tickets/<int:pk>/edit/',      views.TicketUpdateView.as_view(),    name='ticket-update'),
    path('tickets/<int:pk>/delete/',    views.TicketDeleteView.as_view(),    name='ticket-delete'),

    # Special features
    path('issue-ticket/',               views.issue_ticket,  name='issue-ticket'),
    path('tickets/<int:pk>/checkin/',   views.checkin,       name='checkin'),
    path('flights/<int:pk>/manifest/',  views.manifest,      name='manifest'),
    path('flights/search/',             views.flight_search, name='flight-search'),

    # REST API endpoints
    path('api/flights/<int:pk>/occupancy/', views.flight_occupancy_api,        name='flight-occupancy'),
    path('api/flights/',                    views.FlightListCreateAPI.as_view(), name='api-flights'),
    path('api/tickets/',                    views.TicketListCreateAPI.as_view(), name='api-tickets'),
]