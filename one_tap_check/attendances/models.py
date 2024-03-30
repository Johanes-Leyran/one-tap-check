from django.db import models
from rooms.models import Room
from django.contrib.auth import get_user_model
from mixins.timeawarezonemixin import TimezoneAwareMixin
from django.utils import timezone
from utils.cuid import CUID_ATTENDANCE, CUID_ATTENDEE
# Todo: archive the data when deleted
# Todo: index the models for speed


class Attendance(TimezoneAwareMixin):
    cuid2 = models.CharField(
        default=CUID_ATTENDANCE.generate,
        max_length=CUID_ATTENDANCE.length,
        editable=False,
        unique=True,
        primary_key=True
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True
    )
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
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
        related_name='attendees'
    )
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE
    )
    starting_at = models.DateTimeField(  # time in
        default=timezone.now,
    )
    end_at = models.DateTimeField(null=True)  # time out

    def time_out(self) -> None:
        self.end_at = timezone.now()

    def __str__(self) -> str:
        return (
            f"Attendee: {self.user.last_name} at Room: {self.attendance.room.name}"
        )
