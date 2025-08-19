from django.core.mail import send_mail
from django.conf import settings
import django_rq

def send_activation_email(domain, uid, token, email):
    """
    Send an activation email to the user.

    Args:
        domain (str): The domain of the website.
        uid (str): The unique identifier of the user.
        token (str): The token for account activation.
        email (str): The email address of the user.

    Sends an account activation link to the user's email address.
    """
    activation_link = f'{domain}/pages/auth/activate.html?uid={uid}&token={token}'
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(send_mail, f'Account Activation from {domain}', f'Click the link to activate your account: {activation_link}', settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

def send_password_reset_email(domain, uid, token, email):
    """
    Send a password reset email to the user.

    Args:
        domain (str): The domain of the website.
        uid (str): The unique identifier of the user.
        token (str): The token for password reset.
        email (str): The email address of the user.
    """
    reset_link = f'{domain}/pages/auth/confirm_password.html?uid={uid}&token={token}'
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(send_mail,  f'Password Reset from {domain}', f'Click the link to reset your password: {reset_link}', settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)