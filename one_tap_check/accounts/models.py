from django.db import models
from accounts.managers import OneTapUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid


class OneTapUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField('uuid', default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=120)
    last_name = models.CharField('last name', max_length=60)
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = OneTapUserManager()
    
    class Meta:
        permissions = [
            # TODO: implement custom permissions
        ]

    def __str__(self):
        return self.email
    