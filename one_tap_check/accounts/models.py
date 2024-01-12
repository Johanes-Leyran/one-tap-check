from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid


class OneTapUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(default="", max_length=120)
    last_name = models.CharField(default="", max_length=120)
    
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    