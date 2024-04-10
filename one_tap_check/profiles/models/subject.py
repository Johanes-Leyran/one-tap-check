from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(
        max_length=120,
        verbose_name="Name of the subject",
        primary_key=True,
        unique=True
    )
