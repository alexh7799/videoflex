from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage
import os

logo_path = os.path.join(settings.STATIC_ROOT, "logo_icon.png")

def image_attachment():
    image_filename = 'logo_icon.png'
    with open(logo_path, 'rb') as f:
        image_data = f.read()
    msg_image = MIMEImage(image_data)
    msg_image.add_header('Content-ID', f'<{image_filename}>')
    return msg_image

def send_activation_email(domain, uid, token, email, username):
    """
    Send an activation email to the user.

    Args:
        domain (str): The domain of the website.
        uid (str): The unique identifier of the user.
        token (str): The token for account activation.
        email (str): The email address of the user.

    Sends an account activation link to the user's email address.
    """
    try:
        msg_image = image_attachment()
    except Exception as e:
        msg_image = None
    activation_link = f"{domain}/pages/auth/activate.html?uid={uid}&token={token}"
    subject = "Confirm your email"
    html_content = f"""
    <html>
      <body>
        <div style="text-align:center;">
          <img src="cid:logo_icon.png" alt="Videoflix" style="width:180px; margin-bottom:20px;" />
        </div>
        <p>Dear {username},</p>
        <p>Thank you for registering with <b style="color:#2d2dff;">Videoflix</b>. To complete your registration and verify your email address, please click the link below:</p>
        <div style="display:flex;text-align:center;">
          <a href="{activation_link}" style="background:#2d2dff;color:#fff;padding:14px 32px;border-radius:24px;text-decoration:none;font-weight:bold;font-size:18px;display:inline-block;">Activate account</a>
        </div>
        <p>If you did not create an account with us, please disregard this email.</p>
        <p>Best regards,<br>Your Videoflix Team.</p>
      </body>
    </html>
    """
    msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [email])
    if msg_image:
        msg.attach(msg_image)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_password_reset_email(domain, uid, token, email):
    """
    Send a password reset email to the user.

    Args:
        domain (str): The domain of the website.
        uid (str): The unique identifier of the user.
        token (str): The token for password reset.
        email (str): The email address of the user.
    """
    try:
        msg_image = image_attachment()
    except Exception as e:
        msg_image = None
    reset_link = f"{domain}/pages/auth/confirm_password.html?uid={uid}&token={token}"
    subject = "Reset your Password"
    html_content = f"""
    <html>
      <body>                                                                                                                                                                                                                                      
        <p>Hello,</p>
        <p>We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:</p>                                                                                        
        <div style="display:flex; text-align:center;">
         <a href={reset_link} style="background:#2d2dff;color:#fff;padding:14px 32px;border-radius:24px;text-decoration:none;font-weight:bold;font-size:18px;display:inline-block;">Reset password</a>                                                                                                                                                                                                                                            
        </div>
        <p>Please note that for security reasons, this link is only valid for 24 hours.</p>
       <p>If you did not request a password reset, please ignore this email.</p>                                                                                                                                                                 
        <p>Best regards,<br>Your Videoflix team!</p>
        <div style="display:flex; text-align:center; width:180px; margin-top:20px;">                                                                                                                                                                                                        
         <img src="cid:logo_icon.png" alt="Videoflix" style="width:180px; margin-top:20px;" />
       </div>                                                                                                                                                                                                                                    
   </body>
   </html> 
    """
    msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, [email])
    if msg_image:
        msg.attach(msg_image)
    msg.attach_alternative(html_content, "text/html")
    msg.send()