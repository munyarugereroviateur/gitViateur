# Airline Flight & Passenger Ticketing System

Django 4.2 web application for managing airline flights and passengers.

## Student
Name: MUNYARUGERERO Viateur
Reg:  225046763
Course: DSM6332 Cloud Computing & Web Programming
ACE-DS, University of Rwanda

## Tech Stack
- Backend:  Django 4.2 + Django REST Framework
- Database: MySQL
- Server:   Nginx + Gunicorn on Ubuntu VM
- Frontend: Bootstrap 5

## Features
- CRUD for Airplanes, Flights, Passengers, Tickets
- Issue tickets and passenger check-in
- Passenger manifest per flight
- Search flights by origin/destination (Q objects)
- Passport photo upload
- REST API: flight occupancy + DRF list/create endpoints
- Login / Logout / Registration

## Setup
1. pip install -r requirements.txt
2. Set your MySQL password in settings.py
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver