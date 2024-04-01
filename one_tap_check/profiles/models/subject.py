from django.db import models
from django.contrib.auth import get_user_model


class Subject(models.Model):
    subject_name = models.CharField(
        max_length=120,
        verbose_name="Name of the subject",
        primary_key=True,
        unique=True
    )
    teachers = models.ManyToManyField(
        get_user_model(),
        verbose_name="Teachers designated to the subject",
        related_name="designated_subjects",
        null=True
    )
