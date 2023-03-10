from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import EmailValidator, MaxValueValidator , MinValueValidator 
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .mail import *
import random
# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None):

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email,name, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Participant(AbstractBaseUser):

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[EmailValidator()])
    name = models.CharField(max_length=150, null=True , blank=False)
    gender = models.CharField(max_length=10,choices=GENDER, null=True , blank=False)
    college = models.CharField(max_length=350, null=True , blank=False)
    course = models.CharField(max_length=150, null=True , blank=False)
    branch = models.CharField(max_length=150, blank=True)
    mobile = models.PositiveIntegerField(null=True , blank=False)
    year_of_study = models.PositiveIntegerField(null=True , blank=False)
    member_id = models.CharField(max_length=250, blank=True)
    referral_code = models.CharField(max_length=250, blank=True)
    is_ambassador = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    referral_count = models.PositiveIntegerField(default = 0)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Team(AbstractBaseUser):
    name = models.CharField(max_length=150, blank=False, null=True, unique=True)
    size = models.PositiveIntegerField(null=True , blank=False, validators=[MaxValueValidator(3),MinValueValidator(1)])
    team_id = models.CharField(max_length=250, blank=True)
    topic = models.CharField(max_length=1500, blank=True)
    domain = models.CharField(max_length=150, blank=True)
    referral_used = models.CharField(max_length=15, blank=True)
    leader_id = models.OneToOneField(Participant , null=True , blank=False , on_delete=models.RESTRICT, related_name = "leader",)
    member_2 = models.OneToOneField(Participant , null=True , on_delete=models.RESTRICT , related_name = "member_2")
    member_3 = models.OneToOneField(Participant , null=True , on_delete=models.RESTRICT , related_name = "member_3")
    password = models.CharField(max_length=10000000000,null=True, blank=False)

    def __str__(self):
        return self.name + "~" + str(self.size)


@receiver(post_save, sender = Participant)
def generate_member_id(sender, **kwargs):
    member = kwargs['instance']
    yos = member.year_of_study
    member_id = (yos*1000000 + member.id)
    referral = member.email[0:3]+str(member_id*100 + random.randint(1 , 99))
    Participant.objects.filter(id=member.id).update(member_id=member_id,referral_code = referral)
    if member.is_ambassador == True:
        send_member_id(member.email,member_id,referral)
    send_member_id(member.email,member_id,1)

@receiver(post_save, sender = Team)
def generate_team_id(sender, **kwargs):
    team = kwargs['instance']
    size= team.size
    team_id = size*100000+team.id
    Team.objects.filter(id=team.id).update(team_id=team_id)
    send_team_id(team.leader_id.email,team_id)