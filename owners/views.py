from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Owner
from accounts.validators import profile_complete_required
from cars.models import CarCategory
from cars.forms import CarCategoryForm

# Create your views here.
@profile_complete_required
@login_required
def dashboard(request):
    context = {}
    return render(request, 'owners/dashboard.html', context)

@profile_complete_required
@login_required
def profile(request):
    context = {}
    return render(request, 'owners/profile.html', context)

@profile_complete_required
@login_required
def cars(request):
    user = get_object_or_404(Owner, user=request.user)
    cars = CarCategory.objects.filter(owner=user)
    context = {'cars':cars}
    return render(request, 'owners/cars.html', context)

@profile_complete_required
@login_required
def view_car(request, car_pk):
    user = get_object_or_404(CarOwner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user, pk=car_pk)
    context = {'car':car}
    return render(request, 'owners/single_car.html', context)

@profile_complete_required
@login_required
def add_car(request):
    user = get_object_or_404(Owner, user=request.user)
    form = CarCategoryForm()
    if request.POST:
        form = CarCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect ('cars')

    context = {'form':form}
    return render(request, 'owners/add_car.html', context)

@profile_complete_required
@login_required
def edit_car(request, car_pk):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user, pk=car_pk)
    form = CarCategoryForm(instance=car)
    if request.POST:
        form = CarCategoryForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = user
            instance.save()
            return redirect ('cars')

    context = {'car':car, 'form':form}
    return render(request, 'owners/edit_car.html', context)

@profile_complete_required
@login_required
def delete_car(request, car_pk):
    user = get_object_or_404(Owner, user=request.user)
    car = get_object_or_404(CarCategory, owner=user, pk=car_pk)
    CarCategorydelete()
    return redirect ('cars')