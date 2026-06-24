from django.db import models
import uuid


class Airplane(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    airplane_code       = models.CharField(max_length=20, unique=True)
    model               = models.CharField(max_length=100)
    manufacturer        = models.CharField(max_length=100)
    capacity            = models.IntegerField()
    registration_number = models.CharField(max_length=50, unique=True)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.airplane_code} - {self.model}'


class Flight(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('boarding',  'Boarding'),
        ('departed',  'Departed'),
        ('arrived',   'Arrived'),
        ('cancelled', 'Cancelled'),
    ]
    flight_number  = models.CharField(max_length=20, unique=True)
    airplane       = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    origin         = models.CharField(max_length=100)
    destination    = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time   = models.DateTimeField()
    flight_date    = models.DateField()
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    gate_number    = models.CharField(max_length=20, blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.flight_number}: {self.origin} -> {self.destination}'


class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    gender          = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth   = models.DateField()
    passport_number = models.CharField(max_length=50, unique=True)
    nationality     = models.CharField(max_length=100)
    phone           = models.CharField(max_length=20)
    email           = models.EmailField(unique=True)
    passport_photo  = models.ImageField(upload_to='passports/', blank=True, null=True)
    address         = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.passport_number})'


class Ticket(models.Model):
    CLASS_CHOICES = [
        ('economy',  'Economy'),
        ('business', 'Business'),
        ('first',    'First Class'),
    ]
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('cancelled', 'Cancelled'),
        ('used',      'Used'),
    ]
    ticket_number   = models.CharField(max_length=50, unique=True, blank=True)
    passenger       = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='tickets')
    flight          = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    booking_date    = models.DateTimeField(auto_now_add=True)
    seat_number     = models.CharField(max_length=10, blank=True, null=True)
    ticket_class    = models.CharField(max_length=20, choices=CLASS_CHOICES, default='economy')
    price           = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    check_in_status = models.BooleanField(default=False)
    boarding_status = models.BooleanField(default=False)
    ticket_status   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = 'TKT-' + str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.ticket_number} | {self.passenger} | {self.flight}'

    class Meta:
        unique_together = ('flight', 'seat_number')