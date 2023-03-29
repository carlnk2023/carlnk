from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, ReplyTo
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login as dj_login
from accounts.forms import UserAuthenticationForm
from accounts.models import CustomUser
from owners.models import Owner
from cars.forms import CarSearchForm
from cars.models import CarCategory, Location
from django.http import JsonResponse
from django.contrib.sitemaps.views import sitemap
from .sitemaps import CarSitemap, StaticViewSitemap

sendgrid_api = settings.SENDGRID_API_KEY

sitemaps = {
    'cars': CarSitemap,
    'static': StaticViewSitemap,
}

# Create your views here.
def sitemap_xml(request):
    content_type = 'application/xml'
    return sitemap(request, sitemaps=sitemaps, content_type=content_type)

def car_search_ajax(request):
	pickup_location         = request.GET.get('pickup_location')
	transmission_manual     = request.GET.get('transmission_manual')
	transmission_automatic  = request.GET.get('transmission_automatic')
	mileage                 = request.GET.get('mileage')
	vehicle_type            = request.GET.get('vehicle_type')
	no_of_seats             = request.GET.get('no_of_seats')
	min_price               = request.GET.get('min_price')
	max_price               = request.GET.get('max_price')
	rental_min_1            = request.GET.get('rental_min_1')
	rental_min_2            = request.GET.get('rental_min_2')
	rental_min_7            = request.GET.get('rental_min_7')

	if request.method == 'GET':
		cars = CarCategory.objects.exclude(inventory_available='NO')
		if transmission_manual:
			cars = cars.filter(Q(transmission='Manual') | Q(transmission='Both'))
		if transmission_automatic:
			cars = cars.filter(Q(transmission='Automatic') | Q(transmission='Both'))
		if mileage:
			cars = cars.filter(mileage_limit='Unlimited') if mileage == 'unlimited' else cars.filter(mileage_limit='Limited')
		if pickup_location:
			cars = cars.filter(pickup_location__location__icontains=pickup_location).distinct()
		if vehicle_type:
			cars = cars.filter(class_name=vehicle_type)
		if no_of_seats:
			cars = cars.filter(number_of_seats=no_of_seats)
		if min_price:
			cars = cars.filter(price_per_day__gte=min_price)
		if max_price:
			cars = cars.filter(price_per_day__lte=max_price)
		if rental_min_1:
			cars = cars.filter(min_days=1)
		if rental_min_2:
			cars = cars.filter(min_days=2)
		if rental_min_7:
			cars = cars.filter(min_days=7)

		car_list = [{'model_name': car.model_name, 'class_name': car.class_name, 
					'price_per_day': car.price_per_day, 'transmission': car.transmission, 
					'number_of_seats': car.number_of_seats, 'model_image':car.model_image.url,
					'bags':car.bags, 'doors':car.doors, 'security_deposit':car.security_deposit,
					'min_days':car.min_days, 'ratings':car.ratings, 'logo':car.owner.logo.url, 
					'business_name':car.owner.business_name, 'car_pk':car.pk, 'business_name_slug':car.owner.business_name_slug,
					'phone_number':car.owner.phone_number, 'whatsapp_number':car.owner.whatsapp_number, 
					'business_email':car.owner.user.email, 'model_name_slug':car.model_name_slug } for car in cars]
		return JsonResponse({'cars': car_list})
		
	else:
		return JsonResponse({'error': 'Invalid request method'})

def home(request):
	transparent_nav = True
	owners = Owner.objects.all()
	context = {'transparent_nav':transparent_nav, 'owners':owners}
	return render(request, 'renters/home.html', context)

def join(request):
	result = '200'
	transparent_nav = True
	name         	= request.POST.get('name')
	company_name  	= request.POST.get('company_name')
	job_title       = request.POST.get('job_title')
	fleet_size      = request.POST.get('fleet_size')
	phone        	= request.POST.get('phone')
	email        	= request.POST.get('email')

	if request.method == 'POST':
		
		message = Mail(
			from_email		= From("noreply@carlnk.co", "CarLnk Mail"),
			to_emails		= 'carlnk2023@gmail.com',
			subject			= 'New Partnership',
			html_content	='A car rental business wants to join CarLnk!<br><br>' 
							+ job_title + ' ' + name + '<br>Company: ' + company_name + '<br>Fleet Size: '
							+ fleet_size + '<br>Phone number: ' + phone + '<br>Email: ' + email
		)
		try:
			sg = SendGridAPIClient(sendgrid_api)
			response = sg.send(message)
			return redirect('home')
		except Exception as e:
			return JsonResponse({'result': result}, status=400)
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/join.html', context)

def send_email_enquiry(request):
	result = '200'
	name         	= request.POST.get('name')
	phone        	= request.POST.get('phone')
	email        	= request.POST.get('email')
	message  		= request.POST.get('message')
	owner  			= request.POST.get('owner')

	if request.method == 'POST':

		message = Mail(
					from_email		= From("noreply@carlnk.co", "CarLnk"),
					to_emails		= owner,
					subject			= 'Potential client via CarLnk',
					html_content 	= message + '<br><br>' + 'Name: ' + name + '<br>Phone number: ' + phone + '<br>Email: ' + email 
										+ '<br><br><br><strong>Do not reply this email, contact the client using the details provided above.</strong>'
		)
		try:
			sg = SendGridAPIClient(sendgrid_api)
			response = sg.send(message)
		except Exception as e:
			result = 'failed'
			return JsonResponse({'result': result}, status=400)

	return JsonResponse({'result': result, }) 

def about(request):
	transparent_nav = True
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/about.html', context)

def contact(request):
	result = '200'
	transparent_nav = True
	name         = request.POST.get('name')
	phone        = request.POST.get('phone')
	email        = request.POST.get('email')
	message      = request.POST.get('message')

	if request.method == 'POST':
		
		message = Mail(
			from_email		= From("noreply@carlnk.co", "CarLnk Mail"),
			to_emails		= 'carlnk2023@gmail.com',
			subject			= 'Contact Form Submission',
			html_content	='Someone sent us a message from our contact form!<br><br>' 
							+ message + ',<br><br>Email: ' + email + '<br>Phone number: ' + phone
		)
		try:
			sg = SendGridAPIClient(sendgrid_api)
			response = sg.send(message)
			return redirect('home')
		except Exception as e:
			return JsonResponse({'result': result}, status=400)
		
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/contact.html', context)

def terms(request):
	transparent_nav = True
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/terms.html', context)

def cookie(request):
	transparent_nav = True
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/cookie.html', context)

def privacy(request):
	transparent_nav = True
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/privacy.html', context)

def single_car(request, rental_name, car_name, pk):
	transparent_nav = True
	car = get_object_or_404(CarCategory, model_name_slug=car_name, pk=pk)
	context = {'transparent_nav':transparent_nav, 'car':car}
	return render(request, 'renters/single_car.html', context)

def search(request):
	transparent_nav = False
	location = request.GET.get('q')
	 
	cars = CarCategory.objects.filter(pickup_location__location__icontains=location).exclude(inventory_available=False).distinct()
	cars = cars.order_by('price_per_day')
	context = {
		'cars': cars,
		'transparent_nav':transparent_nav,
		'location':location,
	}
	return render(request, 'renters/search.html', context)

def search_location(request):
	location = request.GET.get('location')
	payload = []
	if location:
		location_objs = Location.objects.filter(location__icontains=location)
		
		for location_obj in location_objs:
			payload.append(location_obj.location)

	return JsonResponse({'status' : 200 , 'data' : payload})

def signup(request):
	transparent_nav = False
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/signup.html', context)

def login(request):
	context = {}
	transparent_nav = False
	current_user = request.user
	if current_user.is_authenticated:
		return redirect('dashboard')

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(request, email=email, password=password)

			if user is not None:
				dj_login(request, user)
				return redirect('dashboard')

	else:
		form = UserAuthenticationForm()
	context = {'form':form, 'transparent_nav':transparent_nav}
	return render (request, 'renters/login.html', context)


@login_required
def setup_account(request):
	if request.user.profile_complete is True:
		return redirect('dashboard')
	transparent_nav = False
	context = {'transparent_nav':transparent_nav}
	return render(request, 'renters/setup_account.html', context)