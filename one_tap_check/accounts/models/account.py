from django.db import models
from .managers import OneTapUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.cuid import CUID_USER
# Todo: Test the functionality of the OneTapUser and Tag
# Todo: Add archive


class OneTapUser(AbstractBaseUser, PermissionsMixin):
    cuid2 = models.CharField(
        'cuid of the user',
        default=CUID_USER.generate,
        max_length=CUID_USER.length,
        editable=False,
        unique=True,
        primary_key=True
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
    GENDER_CHOICES = (
        ("F", "Female"),
        ("M", "Male")
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        verbose_name="Gender of the user",
        max_length=6
    )

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = OneTapUserManager()

    def __str__(self) -> models.EmailField:
        return self.email

    class Meta:
        permissions: list = [
            (
                "set_student_status",
                "status of the user as a student"
            ),
            (
                "set_teacher_status",
                "status of the user as a teacher"
            ),
            (
                "set_staff_status",
                "status of the user as a staff"
            )
        ]
