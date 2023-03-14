# from background_task import background
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, ReplyTo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, logout, login as dj_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from owners.models import Owner
from datetime import datetime, timedelta
import uuid

sendgrid_api = settings.SENDGRID_API_KEY

# Create your views here.

def create_account(request):
    result = 'failed'
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirmPassword')
    email = request.POST.get('email')

    if password == confirmPassword:
        hashed_password = make_password(password, salt=None, hasher='default')
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={'password': hashed_password}
        )
        if created:
            user.is_active = False
            user.save()
        else:
            return JsonResponse({'result': result}, status=400) 
             
        current_site = get_current_site(request)
        domain = current_site.domain
        button_url = f'https://{domain}/account/verify-email-address/{user.verification_token}'
        TEMPLATE_ID = 'd-a377966d51054db5a9ed48f1622debf8'

        message = Mail(
            from_email= From("contact@prywaretechnologies.com", "CarLnk"),
            to_emails= user.email,
        )

        message.dynamic_template_data = {
        'button_url': button_url,
        }
        message.template_id = TEMPLATE_ID
        message.reply_to = ReplyTo("contact@prywaretechnologies.com", "CarLnk")
        try:
            sg = SendGridAPIClient(sendgrid_api)
            response = sg.send(message)
        except Exception as e:
            return JsonResponse({'result': result}, status=400)

    return JsonResponse({'result': result, }) 

@login_required
def create_owner(request):
    user = get_object_or_404(CustomUser, email=request.user)
    if request.POST.get('action') == 'post':
        lastName = request.POST.get('lastName')
        firstName = request.POST.get('firstName')
        phoneNumber = request.POST.get('phoneNumber')
        businessName = request.POST.get('businessName')
        registeredAddress = request.POST.get('registeredAddress')
        businessPhoneNumber = request.POST.get('businessPhoneNumber')
        website = request.POST.get('website')
        businessSlogan = request.POST.get('businessSlogan')
    
        personal_ID_formField = request.FILES.get('personal_ID_formField')
        cert_of_incorp = request.FILES.get('cert_of_incorp')
        proof_of_res = request.FILES.get('proof_of_res')
        busi_logo = request.FILES.get('busi_logo')
        
        owner, created = Owner.objects.get_or_create(
            user=user,
            first_name=firstName,
            last_name=lastName,
            personal_phone_number=phoneNumber,
            business_name = businessName,
            address = registeredAddress,
            phone_number = businessPhoneNumber,
            website = website,
            tagline = businessSlogan,
            national_ID = personal_ID_formField,
            certificate_of_incorporation =cert_of_incorp, 
            proof_of_residence =proof_of_res, 
            logo = busi_logo
        ) 
        if created:
            user.profile_complete = True
            user.save()
            owner.save()
        else:
            return JsonResponse({'result': result}, status=400) 

    result = "no"
    return JsonResponse({'result': result, }) 

def verify_email(request, token):
    user = CustomUser.objects.get(verification_token=token)
    user.email_verified = True
    user.is_active = True
    user.save()
    return redirect('setup_account')

def update_verification_token():
    users = CustomUser.objects.filter(email_verified=False)
    for user in users:
        if user.verification_token_created_at + timedelta(hours=24) < datetime.now():
            user.verification_token = uuid.uuid4()
            user.verification_token_created_at = datetime.now()
            user.save()

def resend_verification_email(user):
    user.verification_token = uuid.uuid4()
    user.verification_token_created_at = datetime.now()
    user.save()

@login_required
def logout_user(request):
	logout(request)
	return redirect("home")

@login_required
def logout_reset_password(request):
	logout(request)
	return redirect("reset_password")
