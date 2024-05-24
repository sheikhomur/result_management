from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import UniqueIDModel
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class UserAccount(UniqueIDModel, AbstractUser):
    """Custom user model for our system"""
    
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # make email as username
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

