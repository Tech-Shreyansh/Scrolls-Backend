from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

def send_member_id(email,member_id,check):
    subject = "Here's your scroll id"
    if check==1:
        text  = f'Your Scroll Id is {member_id}.DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.\nSCROLLS'
        style = f'<p>Your Scroll Id is <strong style="font-size: 18px;">{member_id}</strong>.</p><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    else:
        text  = f'Your Scroll Id is {member_id}.DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.\nYour referral code is {check}.Make sure team you refer uses it while registering.\nSCROLLS'
        style = f'<p>Your Scroll Id is <strong style="font-size: 18px;">{member_id}</strong>.</p><p style="font-size: 18px;">DO NOT SHARE IT WITH ANYBODY ELSE TEAM LEADER.</p><p>Your referral code is <strong style="font-size: 18px;">{check}</strong>.</p><p style="font-size: 18px;">Make sure team you refer uses it while registering.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    member_id_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    member_id_msg.attach_alternative(style, "text/html")
    member_id_msg.send()

def send_referral_id(email,referral_id):
    subject = "Here's your referral code"
    text  = f'Your referral code is {referral_id}.Make sure team you refer uses it while registering.\nSCROLLS'
    style = f'<p>Your referral code is <strong style="font-size: 18px;">{referral_id}</strong>.</p><p style="font-size: 18px;">Make sure team you refer uses it while registering.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    referral_code_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    referral_code_msg.attach_alternative(style, "text/html")
    referral_code_msg.send()

def send_team_id(email,team_id):
    subject = "Here's your team id"
    text  = f'Your team id is {team_id}.You can use it to login to your dashboard.\nSCROLLS'
    style = f'<p>Your team id is <strong style="font-size: 18px;">{team_id}</strong>.</p><p style="font-size: 18px;">You can use it to login to your dashboard.</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    team_id_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    team_id_msg.attach_alternative(style, "text/html")
    team_id_msg.send()