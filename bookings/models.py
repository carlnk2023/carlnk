from django.db import models
from cars.models import CarCategory, Location

# Create your models here.
class Booking(models.Model):

    TITLES = (
        ("Mr", "Mr"),
        ("Ms", "Ms"),
        ("Mrs", "Mrs"),
        ("Miss", "Miss"),
    ) 


    BOOKING_STATUS = (
        ("Pending", "Pending"),
        ("Current", "Current"), 
        ("Completed", "Completed"),
        ("Canceled", "Canceled")
    )
    renter_name             = models.CharField(max_length=30)
    renter_title            = models.CharField(max_length=6, choices=TITLES)
    renter_phone_number     = models.CharField(max_length=13)
    renter_email            = models.CharField(max_length=50)
    renter_country          = models.CharField(max_length=100)
    renter_city             = models.CharField(max_length=50)
    renter_address          = models.TextField(max_length=100)
    total_days              = models.PositiveIntegerField()
    total_amount            = models.PositiveIntegerField()
    booked_car              = models.ForeignKey(CarCategory, on_delete=models.CASCADE)
    status                  = models.CharField(max_length=9, choices=BOOKING_STATUS, default='Pending')
    approved                = models.BooleanField(default=False)
    canceled                = models.BooleanField(default=False)
    request_declined        = models.BooleanField(default=False)
    pickup_location         = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickup')
    pickup_date             = models.DateTimeField()
    dropoff_location        = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff')
    dropoff_date            = models.DateTimeField()
    date_created            = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booked_car.owner.business_name
