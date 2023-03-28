from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from .models import OTP
import random

def send_otp(email,check):
    subject = "Here's your password reset mail"
    otp = random.randint(1001 , 9999)
    if check == 1:
        mail_type = "team"
    else:
        mail_type = "account"
    text  = f'Your One Time Password for Reset {mail_type} password on scrolls is {otp}.\nValid for only 2 minutes.\n DO NOT SHARE IT WITH ANYBODY.\n SCROLLS'
    style = f'<p>Your One Time Password for Reset {mail_type} password on scrolls is <strong style="font-size: 18px;">{otp}</strong>.</p><p>Valid for only 2 minutes.</p><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    otp_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    otp_msg.attach_alternative(style, "text/html")
    if check==1:
        OTP_data = OTP.objects.filter(email__iexact=email,is_team=True)
    else:
        OTP_data = OTP.objects.filter(email__iexact=email,is_member=True)
    print(OTP_data)
    if OTP_data.exists():
        OTP_data[0].delete()
    if check==1:
        OTP.objects.create(email=email,is_team=True,otp=otp)
    else:
        OTP.objects.create(email=email,is_member=True,otp=otp)
    otp_msg.send()