from django.contrib import admin
from .models import Owner
# Register your models here.

class OwnerAdmin(admin.ModelAdmin):
	list_display = ('user', 'business_name', 'date_created')
	search_fields = ('business_name', 'last_name', 'phone_number', 'whatsapp_number')

admin.site.register(Owner, OwnerAdmin)