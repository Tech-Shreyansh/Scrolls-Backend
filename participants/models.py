from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import EmailValidator

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, name,password=None):

        if not email:
            raise ValueError('Users must have an email address')

        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, user_name, password=None,):
        """
        Creates and saves a superuser with the given email,name, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
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
    name = models.CharField(max_length=150, null=False , blank=False)
    gender = models.CharField(max_length=1, choices=GENDER, null=False , blank=False)
    college = models.CharField(max_length=350, null=False , blank=False)
    course = models.CharField(max_length=150, null=False , blank=False)
    branch = models.CharField(max_length=150, blank=True)
    year_of_study = models.PositiveIntegerField(null=False , blank=False)
    member_id = models.CharField(max_length=250, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email