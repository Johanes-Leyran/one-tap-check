import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class TimezoneAwareMixin(models.Model):
    def clean(self):
        if self.starting_at >= self.end_at:
            raise ValidationError("starting date must not be ahead of end date")

    def save(self, *args, **kwargs):
        if not isinstance(self.starting_at, datetime.datetime):
            self.starting_at = timezone.make_aware(datetime.datetime.combine(self.starting_at, datetime.time.min))

        if self.end_at is not None and not isinstance(self.end_at, datetime.datetime):
            self.end_at = timezone.make_aware(datetime.datetime.combine(self.end_at, datetime.time.max))

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
