from django.core.mail import send_mail

import django_rq

def send_activation_email(domain, uid, token, email):
    activation_link = f'http://{domain}/api/activate/{uid}/{token}/'
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(send_mail, f'Account Activation from {domain}', f'Click the link to activate your account: {activation_link}', f'noreply@{domain}', [email], fail_silently=True)

def send_password_reset_email(domain, uid, token, email):
    reset_link = f'http://{domain}/api/password_reset_confirm/{uid}/{token}/'
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(send_mail,  f'Password Reset from {domain}', f'Click the link to reset your password: {reset_link}', f'noreply@{domain}', [email], fail_silently=True)