from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
import random

def send_member_id(email,member_id,check):
    subject = "Successful member registration for SCROLLS'24"
    if check==1:
        text = f'Dear participant,You have successfully registered yourself for SCROLLS24. Given below is your Scrolls ID:Scrolls id = {member_id}Keep the above ID safe and secure as it will be used for the next phase of registration i.e. team registration.Regards,Team SCROLLS'
        style = f'<p>Dear participant,<br>You have successfully registered yourself for SCROLLS24. Given below is your Scrolls ID:<br><strong style="font-size: 18px;">Scrolls id = {member_id}</strong>.</p><p style="font-size: 18px;"> <br><br>Keep the above ID safe and secure as it will be used for the next phase of registration i.e. team registration.<br><br>Regards,<br>Team SCROLLS</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
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
    subject = "Successful Team registration for SCROLLS'24."
    text = f'Dear participant,Congratulations on successful completion of the registration process for SCROLLS24. The unique Team ID is as follows:<Team id = {team_id}>●The Team ID must be kept private for further use.●The team members can login using the team leader E-mail ID or this Team ID along with team password to access the dashboard.●The dashboard will be the platform to submit your synopsis and final research paper..Regards and Best Wishes,Team SCROLLS'
    style = f'<p>Dear participant,<br>Congratulations on successful completion of the registration process for SCROLLS24. The unique Team ID is as follows:<br><strong style="font-size: 22px;">Team id = {team_id}</strong>.</p><p style="font-size: 18px;"> <br><br>●The Team ID must be kept private for further use.<br>●The team members can login using the team leader E-mail ID or this Team ID along with team password to access the dashboard.<br>●The dashboard will be the platform to submit your synopsis and final research paper.<br><br>Regards and Best wishes,<br>Team SCROLLS</p><div style="text-align:center; font-size:40px; color:grey; margin-top:20px;"><strong>SCROLLS</strong></div>'
    email_by = settings.EMAIL_HOST
    team_id_msg = EmailMultiAlternatives(subject, text,email_by,[email])
    team_id_msg.attach_alternative(style, "text/html")
    team_id_msg.send()