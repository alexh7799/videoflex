from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

def send_activation_email(saved_account, request):
    uid = urlsafe_base64_encode(force_bytes(saved_account.pk))
    token = saved_account.activation_token
    domain =  get_current_site(request).domain
    activation_link = f'http://{domain}/api/activate/{uid}/{token}/'
    send_mail( f'Account Activation from {domain}', f'Click the link to activate your account: {activation_link}', f'noreply@{domain}', [saved_account.email], fail_silently=True,)

def send_password_reset_email(email, request):
    user = User.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = get_current_site(request).domain
    reset_link = f'http://{domain}/api/password_reset_confirm/{uid}/{token}/'
    send_mail( f'Password Reset from {domain}', f'Click the link to reset your password: {reset_link}', f'noreply@{domain}', [email], fail_silently=True,)
    return User.objects.filter(email=email).exists()