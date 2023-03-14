import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail
from rq import get_current_job

def send_verification_email(email, subject, message):
    print("Background Job done")
    # send_mail(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), [email])
