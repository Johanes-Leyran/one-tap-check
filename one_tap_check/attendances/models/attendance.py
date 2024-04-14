from django.db import models
from utils.cuid import CUID_ATTENDANCE
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from rooms.models.room import Room

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
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="attendance_records"
    )
    starting_at = models.DateField(default=timezone.now)
    end_at = models.DateField(
        default=None,
        null=True
    )

    def __str__(self):
        return (
            f"Attendance of Teacher: {self.teacher.name} at Room: {self.room.name}"
        )
