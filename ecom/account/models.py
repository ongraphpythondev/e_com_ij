from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import settings
from knox.models import AuthToken
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from account.utils import password_generator
from ecom.utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
                raise ValueError('users must have a Password')
       
        print("this is ok")
        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_user_without_password(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
       
        print("running")
        user_obj = self.model(
            phone=phone
        )
        user_obj.password = password_generator(25)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
          password=password,
            is_staff=True,
            is_admin=True,


        )
        print(user)
        return user


class User(AbstractBaseUser):
    #password = None
    phone_regex = RegexValidator(  regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    first_login = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    

class PhoneOTP(models.Model):
        phone_regex = RegexValidator(  regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
        phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
        otp = models.IntegerField()


