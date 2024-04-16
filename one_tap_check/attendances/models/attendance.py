from django.db import models
from utils.cuid import CUID_ATTENDANCE
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from simple_history.models import HistoricalChanges


# Todo: Make a permission separate from the models
# Todo: Add permissions for each models


class Attendance(TimezoneAwareMixin):
    cuid2 = models.CharField(
        default=CUID_ATTENDANCE.generate,
        max_length=CUID_ATTENDANCE.length,
        editable=False,
        unique=True,
        primary_key=True
    )
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendances"
    )
    section = models.ForeignKey(
        'profiles.Section',
        null=True,
        on_delete=models.SET_NULL,
    )
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_records"
    )
    starting_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(
        default=None,
        null=True
    )
    subject = models.ForeignKey(
        'profiles.Subject',
        blank=True,
        on_delete=models.SET_NULL,
        null=True
    )
    history = HistoricalChanges()

    def __str__(self):
        return (
            f"Attendance of Teacher: {self.teacher.last_name} at Room: {self.room.name}"
        )
