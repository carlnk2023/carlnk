from django import forms
from .models import CarCategory

TRANSMISSION_TYPES = (
	("Automatic", "Automatic"),
	("Manual", "Manual"),
	("Both", "Both"),
)
 
CAR_CLASS = (
	("Convertible", "Convertible"),
	("Standard", "Standard"),
	("Truck", "Truck"),
	("SUV", "SUV"),
	("Commuter Omnibus", "Commuter Omnibus"),
	("Vans", "Vans"),
	("Luxury Car", "Luxury Car")
)

YES_NO = (
	("Yes", "Yes"),
	("No", "No"),
)

class CarCategoryForm(forms.ModelForm):
	transmission =  forms.ChoiceField(label='Type of transmission of cars in the class', choices = TRANSMISSION_TYPES)
	free_cancellation =  forms.ChoiceField(label='Free cancellation up to 48 hours before pick-up', choices = YES_NO)	
	inventory_available =  forms.ChoiceField(label='Are there cars available that belong to this class', choices = YES_NO)
	mileage =  forms.IntegerField(label='Kilometers are included in the price')
	number_of_seats =  forms.IntegerField(label='Number of seats in model')
	large_bags =  forms.IntegerField(label='How many large bags can fit in the boot?')
	small_bags =  forms.IntegerField(label='How many small bags can fit in the boot?')

	class Meta:
		model = CarCategory
		fields = ['model_name','class_name', 'price_per_day', 'number_of_seats', 'transmission',
					'mileage', 'model_image', 'pickup_location', 'free_cancellation', 
					'inventory_available', 'large_bags', 'small_bags']


class CarSearchForm(forms.Form):
    class_name = forms.ChoiceField(choices=CarCategory.CAR_CLASS, required=False)
    transmission = forms.ChoiceField(choices=CarCategory.TRANSMISSION_TYPES, required=False)
    mileage_limit = forms.ChoiceField(choices=CarCategory.MILEAGE_TYPE, required=False)
    pickup_location = forms.CharField(required=False)
    date_from = forms.DateField(required=False, widget = forms.SelectDateWidget())
    date_to = forms.DateField(required=False)
    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)
    number_of_seats = forms.IntegerField(required=False)