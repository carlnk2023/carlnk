from django.contrib import admin
from .models import CarCategory, Location
# Register your models here.

class CarCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner','model_name', 'class_name', 'transmission', 'date_created')
	list_filter = ('owner', 'transmission', 'mileage_limit', 'inventory_available')
	search_fields = ('model_name', 'class_name')
 
admin.site.register(CarCategory, CarCategoryAdmin)

class LocationAdmin(admin.ModelAdmin):
	list_display = ('id', 'location','date_created')
	list_filter = ('location',)

admin.site.register(Location, LocationAdmin)