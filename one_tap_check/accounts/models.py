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
    section = models.ForeignKey(
        "profiles.Section",
        verbose_name="Section of the user",
        on_delete=models.SET_NULL,
        null=True
    )
    subjects = models.ManyToManyField(
        "profiles.Subject",
        verbose_name="Subjects designated to the user"
    )

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = OneTapUserManager()

    def __str__(self) -> models.EmailField:
        return self.email

    class Meta:
        permissions: list = [
            (
                "accounts.set_student_status",
                "status of the user as a student"
            ),
            (
                "accounts.set_teacher_status",
                "status of the user as a teacher"
            ),
            (
                "accounts.set_staff_status",
                "status of the user as a staff"
            )
        ]
