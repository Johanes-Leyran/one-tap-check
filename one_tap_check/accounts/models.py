from django.db import models
from .managers import OneTapUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
# Todo: study cuid2


class OneTapUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        'uuid',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(
        'email address',
        unique=True
    )
    first_name = models.CharField(
        'first name',
        max_length=120
    )
    last_name = models.CharField(
        'last name',
        max_length=60
    )
    # Todo: add RFID tag model
    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = OneTapUserManager()
    
    # class Meta:
    #     permissions = [
    #         ('can_create_n_end_session', 'Can create or end a Session in a room'),
    #     ]

    def __str__(self):
        return self.email
    