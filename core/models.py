from django.db import models
from django.contrib.auth.models import User

class TravelOption(models.Model):
    TRAVEL_TYPE_CHOICES = [('Flight', 'Flight'), ('Train', 'Train'), ('Bus', 'Bus')]
    travel_id = models.AutoField(primary_key=True)
    type = models.CharField(choices=TRAVEL_TYPE_CHOICES, max_length=10)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        # Return a meaningful string instead of integer
        return f"{self.type} from {self.source} to {self.destination} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    STATUS_CHOICES = [('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=12)
    
    def __str__(self):
        return str(self.booking_id)  # Correctly converted to string
