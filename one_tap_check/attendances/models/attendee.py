from django.db import models
from simple_history.models import HistoricForeignKey

from .attendance import Attendance
from django.contrib.auth import get_user_model
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from django.utils import timezone
from utils.cuid import CUID_ATTENDEE
from datetime import timedelta
# Todo: archive the data when deleted
# Todo: index the models for speed


class Attendee(TimezoneAwareMixin):
    cuid2 = models.CharField(
        default=CUID_ATTENDEE.generate,
        max_length=CUID_ATTENDEE.length,
        editable=False,
        unique=True,
        primary_key=True
    )
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='attendee_records'
    )
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE
    )
    starting_at = models.DateTimeField(  # time in
        default=timezone.now,
    )
    end_at = models.DateTimeField(  # time out
        null=True,
        default=None
    )
    history = HistoricForeignKey(
        'attendances.Attendance',
        on_delete=models.SET_NULL,
        null=True
    )
    STATUS_CHOICES = (
        ("Late", "Late"),
        ("On Time", 'One Time'),
        ("Absent", "Absent")
    )
    status = models.CharField(
        max_length=8,
        blank=True
    )

    def time_out(self) -> None:
        self.end_at = timezone.now()

    def set_status(self):
        if not self.status:
            if self.starting_at - self.attendance.starting_at < timedelta(minutes=15):
                self.status = "Late"
            else:
                self.status = "On Time"
        else:
            self.status = "Absent"

        self.save()

    def __str__(self) -> str:
        return (
            f"Attendee: {self.user.last_name} at Room: {self.attendance.room.name}"
        )
