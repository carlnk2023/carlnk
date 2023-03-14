from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cars.models import CarCategory
from owners.models import Owner
from .models import Booking

# Bookings
@login_required
def bookings(request):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    bookings = Booking.objects.filter(booked_car=car, approved=True)
    context = {'bookings':bookings}
    return render(request, 'bookings/bookings.html', context)

@login_required
def view_booking(request, booking_pk):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    booking = get_object_or_404(Booking, booked_car=car, approved=True, id=booking_pk)
    context = {'booking':booking}
    return render(request, 'bookings/view_booking.html', context)


@login_required
def cancel_booking(request, booking_pk):
    user = get_object_or_404(CarOwner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    booking = get_object_or_404(Booking, booked_car=car, id=booking_pk)
    booking.canceled = True
    booking.save()
    return redirect ('bookings')

# Requests

@login_required
def car_requests(request):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    car_requests = Booking.objects.filter(booked_car=car, approved=False)
    context = {'car_requests':car_requests}
    return render(request, 'bookings/car_requests.html', context)

@login_required
def view_car_request(request, booking_pk):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    car_request = get_object_or_404(Booking, booked_car=car, approved=False, request_declined=False, id=booking_pk)
    context = {'car_request':car_request}
    return render(request, 'bookings/view_car_request.html', context)

@login_required
def accept_request(request, booking_pk):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    price = request.POST.get('price')
    days = request.POST.get('days')
    int_days = int(days)
    int_price = int(price)
    if request.POST:
        booking = get_object_or_404(Booking, booked_car=car, id=booking_pk, approved=False)
        booking.total_days = int_days
        booking.total_amount = int_price * int_days
        booking.approved = True
        booking.status = "Current"
        booking.save()
        return redirect ('bookings')

@login_required
def decline_request(request, booking_pk):
    user = get_object_or_404(CarOwner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user)
    booking = get_object_or_404(Booking, booked_car=car, id=booking_pk)
    booking.request_declined = True
    booking.save()
    return redirect ('car_requests')
