from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

from .managers import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20, null=True, blank=True, validators=[RegexValidator(regex='^\d{10}$')])
    dob = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
