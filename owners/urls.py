from django.urls import path
from .import views

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('cars/', views.cars, name='cars'),
	path('profile/', views.profile, name='profile'),
	path('cars/add/', views.add_car, name='add_car'),
	path('cars/view/<int:car_pk>/', views.view_car, name='view_car'),
	path('cars/edit/<int:car_pk>/', views.edit_car, name='edit_car'),
	path('cars/delete/<int:car_pk>/', views.delete_car, name='delete_car'),
]
  