from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

def send_member_id(email,member_id):
    subject = "Here's your scroll id"
    text  = f'Your Scroll Id is {member_id}.DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.\nSCROLLS'
    style = f'<p>Your Scroll Id is <strong style="font-size: 18px;">{member_id}</strong>.</p><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    member_id_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    member_id_msg.attach_alternative(style, "text/html")
    member_id_msg.send()

