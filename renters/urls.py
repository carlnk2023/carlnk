from django.urls import path
from .import views
 
urlpatterns = [
	path('', views.home, name='home'),
	path('join/', views.join, name='join'),
	path('about-us/', views.about, name='about'),
	path('contact-us/', views.contact, name='contact'),
	path('terms-and-conditions/', views.terms, name='terms'),
	path('privacy-policy/', views.privacy, name='privacy'),
	path('cookie-policy/', views.cookie, name='cookie'),
	path('search/', views.search, name='search'),
	path('send-email-enquiry/', views.send_email_enquiry, name='send_email_enquiry'),
	path('search-location/', views.search_location, name='search_location'),
	path('<slug:rental_name>/<slug:car_name>/<int:pk>/', views.single_car, name='single_car'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login, name='login'),
	path('setup-account/', views.setup_account, name='setup_account'),
	path('car-search-ajax/', views.car_search_ajax, name='car_search_ajax'),
	path('sitemap.xml', views.sitemap_xml, name='django.contrib.sitemaps.views.sitemap'),
]
  