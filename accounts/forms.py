from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", )

class UserAuthenticationForm(forms.ModelForm):
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	password =  forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

	class Meta:
		model = CustomUser
		fields = ('email', 'password')
 
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Incorrect email or password")