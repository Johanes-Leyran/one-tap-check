from django.db import models


class Section(models.Model):
    section_name = models.CharField(
        max_length=120,
        verbose_name="Name of the section",
        primary_key=True,
        unique=True
    )
