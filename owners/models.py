import os
from uuid import uuid4
from django.db import models
from datetime import datetime
from django.utils.text import slugify
from accounts.models import CustomUser
from django.conf import settings
MEDIA_ROOT  = settings.MEDIA_ROOT
from django.utils.translation import gettext_lazy as _
from .validators import validate_file_size
# Create your models here.
 
def user_directory_path(instance, filename):
    # generate a unique filename using a UUID and timestamp
    extension = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f'{uuid4().hex}{timestamp}{extension}'
    
    # file will be uploaded to MEDIA_ROOT/user_<id>/<unique_filename>
    return f'user_{instance.user.id}/{unique_filename}'


class Owner(models.Model):
    user                         =  models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name                   =  models.CharField(max_length=50)
    last_name                    =  models.CharField(max_length=50)
    personal_phone_number        =  models.CharField(max_length=50)
    business_name                =  models.CharField(max_length=50)
    business_name_slug           =  models.SlugField(max_length=50, unique=True, blank=True)
    address                      =  models.TextField(max_length=100)
    phone_number                 =  models.CharField(max_length=50)
    whatsapp_number              =  models.CharField(max_length=50)
    website                      =  models.CharField(max_length=50, null=True, blank=True)
    national_ID                  =  models.ImageField(upload_to=user_directory_path, verbose_name="National ID", validators=[validate_file_size], null=True, blank=True)
    certificate_of_incorporation =  models.ImageField(upload_to=user_directory_path, verbose_name="Certificate of Incorporation", validators=[validate_file_size], null=True, blank=True)
    proof_of_residence           =  models.ImageField(upload_to=user_directory_path, verbose_name="Proof of Residence", validators=[validate_file_size], null=True, blank=True)
    logo                         =  models.ImageField(upload_to=user_directory_path, verbose_name="Logo", validators=[validate_file_size], null=True, blank=True)
    date_created                 =  models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created', )
          
    def save(self, *args, **kwargs):
        # generate the slug for the business_name field
        self.business_name_slug = slugify(self.business_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name