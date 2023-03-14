from django.urls import path
from .import views

urlpatterns = [
	path('', views.bookings, name='bookings'),
	path('view/<int:booking_pk>/', views.view_booking, name='view_booking'),
	path('cancel/<int:booking_pk>/', views.cancel_booking, name='cancel_booking'),
	path('requests/', views.car_requests, name='car_requests'),
	path('requests/<int:booking_pk>/', views.view_car_request, name='view_car_request'),
	path('accept-request/<int:booking_pk>/', views.accept_request, name='accept_request'),
	path('decline-request/<int:booking_pk>/', views.decline_request, name='decline_request'),
]
  