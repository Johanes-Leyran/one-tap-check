from django.db import models
from django.contrib.auth import get_user_model


class Section(models.Model):
    section_name = models.CharField(
        max_length=120,
        verbose_name="Name of the section",
        primary_key=True,
        unique=True
    )
    students = models.ForeignKey(
        get_user_model(),
        verbose_name="Students of the section",
        related_name="section",
        on_delete=models.SET_NULL,
        null=True
    )
    advisor = models.ForeignKey(
        get_user_model(),
        verbose_name="Advisor of the section",
        related_name="advisory_section",
        on_delete=models.SET_NULL,
        null=True
    )
