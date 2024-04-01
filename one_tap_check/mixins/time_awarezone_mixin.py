from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


class TimezoneAwareMixin(models.Model):
    def clean(self):
        if self.starting_at >= self.end_at:
            raise ValidationError("starting date must not be ahead of end date")

    def save(self, *args, **kwargs):
        if not self.starting_at.tzinfo:
            self.starting_at = timezone.make_aware(self.starting_at)

        if (self.end_at is not None
                and not self.end_at.tzinfo):
            self.end_at = timezone.make_aware(self.end_at)

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
