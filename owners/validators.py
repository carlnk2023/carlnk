from django.core.exceptions import ValidationError
from django.contrib import messages

def validate_file_size(value):
	filesize = value.size

	if filesize > 104857600:
		raise ValidationError("The maximum upload size is 100MB")
	else:
		return value
