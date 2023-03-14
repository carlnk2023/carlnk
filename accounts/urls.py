from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.create_account, name='create_account'),
	path('logout/', views.logout_user, name='logout_user'),
	path('verify-email-address/<token>/', views.verify_email, name='verify_email'),
	path('create-owner/', views.create_owner, name='create_owner'),

	#Password Reset
	path('logout-reset-password', views.logout_reset_password, name='logout_reset_password'),
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="renters/password_reset.html"), name="reset_password"),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="renters/password_reset_sent.html"), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="renters/password_reset_form.html"), name="password_reset_confirm"),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="renters/password_reset_complete.html"), name="password_reset_complete"),
]
  