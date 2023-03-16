import os
from uuid import uuid4
from django.db import models
from datetime import datetime
from owners.models import Owner
from django.utils.text import slugify
from owners.validators import validate_file_size
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

def user_directory_path_cars(instance, filename):
    extension = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'{uuid4().hex}{timestamp}{extension}'
    
    # file will be uploaded to MEDIA_ROOT/user_<id>/cars/<unique_filename>
    return f'user_{instance.owner.user.id}/cars/{unique_filename}'

    
class Location(models.Model):
    location        = models.CharField(max_length=250)
    date_created    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location


class CarCategory(models.Model):
    TRANSMISSION_TYPES = (
        ("Automatic", "Automatic"),
        ("Manual", "Manual"),
        ("Both", "Both"),
    )

    CAR_CLASS = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Truck", "Truck"),
        ("SUV", "SUV"),
        ("Van", "Van"),
    ) 

    MILEAGE_TYPE = (
        ("Limited", "Limited"),
        ("Unlimited", "Unlimited")
    )
    
    YES_NO = (
        ("Yes", "Yes"),
        ("No", "No"),
    )

    model_name          = models.CharField(max_length=50)
    model_name_slug     = models.SlugField(max_length=50, blank=True)
    class_name          = models.CharField(max_length=50, choices=CAR_CLASS, default='Standard')
    owner               = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='car')
    price_per_day       = models.PositiveIntegerField(default=0, verbose_name="Price per day")
    number_of_seats     = models.PositiveIntegerField(default=1)
    transmission        = models.CharField(max_length=9, choices=TRANSMISSION_TYPES, default='Automatic', verbose_name="Type of transmission")
    mileage_limit       = models.CharField(max_length=9, choices=MILEAGE_TYPE, default='Limited', verbose_name="Mileage/Kilometres limit")
    mileage             = models.PositiveIntegerField(default=0, null=True, blank=True,  verbose_name="Mileage/Kilometres")
    inventory_available = models.CharField(max_length=3, choices=YES_NO, default='Yes')
    pickup_location     = models.ManyToManyField(Location, verbose_name="Available pick-up locations")
    model_image         = models.ImageField(upload_to=user_directory_path_cars, verbose_name="Model image", validators=[validate_file_size])
    bags                = models.PositiveIntegerField(default=0)
    doors               = models.PositiveIntegerField(default=0)
    security_deposit    = models.PositiveIntegerField(default=0)
    min_days            = models.PositiveIntegerField(default=0)
    ratings             = models.CharField(max_length=5)
    date_created        = models.DateTimeField(auto_now_add=True)
    last_modified       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', )
        verbose_name = 'Car Category'
        verbose_name_plural = 'Car Categories'

    def save(self, *args, **kwargs):
        # generate the slug for the business_name field
        self.model_name_slug = slugify(self.model_name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.model_name