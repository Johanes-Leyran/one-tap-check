from django.db import models
from utils.cuid import CUID_SCANNER


class Scanner(models.Model):
    cuid2 = models.CharField(
        primary_key=True,
        default=CUID_SCANNER.generate,
        max_length=CUID_SCANNER.length,
        editable=False,
        unique=True
    )
    STATUS_CHOICE = (
        ("WORKING", "Working"),
        ("NOT WORKING", "Not Working")
    )
    status = models.CharField(
        choices=STATUS_CHOICE,
        max_length=14
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Scanner - {self.pk}"
