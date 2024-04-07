from django.core.mail import send_mail
from django.conf import settings
from .models import OTP, Team, Participant
import random

def send_otp(email, check, name):
    subject = "Forgot Password"
    otp = random.randint(1001, 9999)
    if check == 1:
        mail_type = "team"
        
    else:
        mail_type = "account"
    html_content = f"""
    <html>
    <head>
        <title>Forgot Password</title>
    </head>
    <body>
    <div>
        Dear {name},
        <br><br>
        You have requested to reset your password for your SCROLLS’24 account.<br>
        Your one-time password to reset your account password is: {otp}
        <br>
        <p style="color: red;">*valid only for 2 minutes.</p>(Do not share it with anybody)
        
        <br>
        <br>
        If you did not request this password reset or have any other concern, please contact us immediately.
            <br>
            <br>
        Best regards,
        Team SCROLLS
        </div>
    </body>
    </html>
    """
    
    send_mail(subject, "", settings.EMAIL_HOST_USER, [email],html_message=html_content)
    
    if check == 1:
        OTP_data = OTP.objects.filter(email__iexact=email, is_team=True)
    else:
        OTP_data = OTP.objects.filter(email__iexact=email, is_member=True)
        
    if OTP_data.exists():
        OTP_data[0].delete()
    
    if check == 1:
        OTP.objects.create(email=email, is_team=True, otp=otp)
    else:
        OTP.objects.create(email=email, is_member=True, otp=otp)
