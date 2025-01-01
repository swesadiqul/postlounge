from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import random


# Generate OTP
def generate_otp():
    return random.randint(100000, 999999)


# Email sending function
def send_email(recipient_list, recipient_name):
    otp_code = generate_otp()  # Generate OTP
    subject = "Your OTP for Email Verification"
    
    # Render HTML content for the email
    html_message = render_to_string('accounts/send-otp.html', {
        'otp_code': otp_code,
        'name': recipient_name,
        'company_name': 'Postlounge',
        'support_email': 'support@postlounge.com',
        'website_url': 'https://postlounge.com',
        'logo_url': 'https://shorturl.at/XPBbN',
        'website_url': 'http://localhost:8000',
        'current_year': timezone.now().year,

    })
    
    # Plain text version of the email (for clients that don't support HTML)
    text_message = f"Your OTP code is: {otp_code}\n\nIf you didn't request this, please ignore this email."

    from_email = settings.EMAIL_HOST_USER  # Your email host user (configured in settings)

    send_mail(
        subject,
        text_message,  # Plain text version
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,  # HTML version for modern email clients
        fail_silently=False,
    )

    return otp_code


# Get JWT tokens for user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

