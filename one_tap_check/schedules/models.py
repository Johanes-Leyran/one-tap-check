from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


class ScheduleSheet(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL)
    name = models.CharField(max_length=120)
    start_day_at = models.DateField()
    stop_day_at = models.DateField()


class ScheduleRoom(models.Model):
    schedule = models.ForeignKey(ScheduleSheet, on_delete=models.CASCADE)
    room = models.ForeignKey(None, on_delete=models.SET_NULL)
    teacher = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL)
    starting_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def clean(self):
        if self.starting_at >= self.end_at:
            raise ValidationError("starting date must not be ahead of end date")
    
    def save(self, *args, **kwargs):
        self.starting_at = timezone.make_aware(self.starting_at)
        self.end_at = timezone.make_aware(self.end_at)
        super().save(*args, **kwargs)
       