from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
import random

from participants.models import Participant, Team
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


def send_member_id(email, member_id, check):
    subject = "Successful member registration for SCROLLS'24"
    if check == 1:
        member_data = Participant.objects.get(email=email)
        subject = "Welcome to SCROLLS’24."
        message = f"""
        <html>
    <head>
    </head>
    <body>
    <div>
        Subject: {subject}<br><br>
        
        Dear {member_data.name},<br><br>
        
        Greetings from SCROLLS, AKGEC!<br><br>
        
        Congratulations, you have successfully registered for SCROLLS’24.<br>
        Your unique SCROLLS ID: {member_data.member_id}<br><br>
        
        Keep the above ID safe as it will be used for the next phase of registration i.e. team registration.<br><br>
        
        Follow our Instagram Page for more info Click here.<br>
        Visit our website at scrollsakgec.in<br><br>
        
        Regards,<br>
        Team SCROLLS
         </div>
    </body>
    </html>
        """

        send_mail(
            subject,
            "",
            settings.EMAIL_HOST_USER,
            [member_data.email],
            html_message=message,
        )

    else:
        ca_data = Participant.objects.get(email=email)
        subject = "Welcome to SCROLLS’24 Campus Ambassador Program."
        message = f"""
        <html>
    <head>
    </head>
    <body>
    <div>
        Dear {ca_data.name},<br><br>
        
        Greetings from SCROLLS, AKGEC!<br><br>
        
        Congratulations! You've taken the first step towards an exciting journey by registering as a<br> Campus Ambassador for SCROLLS’24.<br><br>
        
        Your unique SCROLLS ID: {ca_data.member_id}<br><br>
        
        Keep your SCROLLS ID safe as it will be used for the next phase of registration i.e. team registration.<br><br>
        
        Your unique Referral ID: {ca_data.referral_code}<br><br>
        
        We encourage you to make the most of your Referral ID by inviting your peers to participate<br> in SCROLLS’24. Your efforts in referring participants not only contribute to the success of the <br>event but also offer you exclusive perks and discounts on your registration fees based on the <br>number of teams registered through your referrals.<br><br>
        
        We're thrilled to have you onboard and look forward to an enriching collaboration ahead!<br><br>
        
        For any queries or assistance, feel free to reach out to us.<br><br>
        
        Follow our Instagram Page for more info Click here.<br>
        Visit our website at scrollsakgec.in<br><br>
        
        Regards,<br>
        Team SCROLLS
        </div>
    </body>
    </html>
        """
        send_mail(
            subject, "", settings.EMAIL_HOST_USER, [ca_data.email], html_message=message
        )


def send_referral_id(email, referral_id):
    ca_data = Participant.objects.get(email=email)
    subject = "Welcome to SCROLLS’24 Campus Ambassador Program."
    message = f"""
     <html>
    <head>
        <title>Forgot Password</title>
    </head>
    <body>
    <div>
    
    Dear {ca_data.name},<br><br>
    
    Greetings from SCROLLS, AKGEC!<br><br>
    
    Congratulations! You've taken the first step towards an exciting journey by registering <br>as a Campus Ambassador for SCROLLS’24.<br><br>
    
    Your unique SCROLLS ID: {ca_data.member_id}<br><br>
    
    Keep your SCROLLS ID safe as it will be used for the next phase of registration i.e. team <br>registration.<br><br>
    
    Your unique Referral ID: {referral_id}<br><br>
    
    We encourage you to make the most of your Referral ID by inviting your peers to participate in<br> SCROLLS’24. Your efforts in referring participants not only contribute to the success of the<br> event but also offer you exclusive perks and discounts on your registration fees based on the<br> number of teams registered through your referrals.<br><br>
    
    We're thrilled to have you onboard and look forward to an enriching collaboration ahead!<br><br>
    
    For any queries or assistance, feel free to reach out to us.<br><br>
    
    Follow our Instagram Page for more info Click here.<br>
    Visit our website at scrollsakgec.in<br>
    
    Regards,<br>
    Team SCROLLS
    </div>
    </body>
    </html>
    """

    send_mail(
        subject, "", settings.EMAIL_HOST_USER, [ca_data.email], html_message=message
    )


def send_team_id(team_id):
    team_data = Team.objects.get(team_id=team_id)
    subject = "Successful Team registration for SCROLLS'24."
    message_plain = f"""
    Dear {team_data.leader_id.name},
    
    Congratulations! Your team {team_data.name} has successfully completed the registration process 
    for SCROLLS'24. The unique Team ID is as follows:
    
    Team ID: {team_id}
    
    <ul>
    <li>The Team ID must be kept private for further use.</li>
    <li>The team members can log in using the team leader's E-mail ID or this Team ID along with the team password to access the dashboard.</li>
    <li>The dashboard will be the platform to submit your synopsis and final research paper.</li>
    </ul>
    
    We are glad to have you on this riveting journey.
    
    Regards and Best wishes,
    Team SCROLLS
    """

    message_html = f"""
    <html>
    <head>
        <title>Successful Team registration for SCROLLS'24.</title>
    </head>
    <body>
    <div>
    <p>Dear {team_data.leader_id.name},</p>
    <p>Congratulations! Your team {team_data.name} has successfully completed the registration process 
    for SCROLLS'24. The unique Team ID is as follows:</p>
    <p>Team ID: {team_id}</p>
    <ul>
    <li>The Team ID must be kept private for further use.</li>
    <li>The team members can log in using the team leader's E-mail ID or this Team ID along with the team password to access the dashboard.</li>
    <li>The dashboard will be the platform to submit your synopsis and final research paper.</li>
</ul>
    <p>We are glad to have you on this riveting journey.</p>
    <p>Regards and Best wishes,<br>
    Team SCROLLS</p>
    </div>
    </body>
    </html>
    """

    send_mail(
        subject,
        message_plain,
        settings.EMAIL_HOST_USER,
        [team_data.leader_id.email],
        html_message=message_html,
    )


@receiver(post_save, sender=Participant)
def generate_member_id(sender, **kwargs):
    member = kwargs["instance"]
    yos = member.year_of_study
    member_id = (yos * 100000 + member.id) * 1000 + random.randint(1, 999)
    referral = member.email[0:3] + str(member_id * 100 + random.randint(1, 99))
    Participant.objects.filter(id=member.id).update(
        member_id=member_id, referral_code=referral
    )
    if member.is_ambassador == True:
        send_member_id(member.email, member_id, referral)
    else:
        send_member_id(member.email, member_id, 1)


@receiver(post_save, sender=Team)
def generate_team_id(sender, **kwargs):
    team = kwargs["instance"]
    size = team.size
    if team.team_id == "" and size:
        team_id = "SC" + str((size * 10000 + team.id) * 1000 + random.randint(1, 999))
        Team.objects.filter(id=team.id).update(team_id=team_id)
        send_team_id(team_id)
