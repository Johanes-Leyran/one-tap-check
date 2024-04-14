from django.db import models
from .attendance import Attendance
from django.contrib.auth import get_user_model
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from django.utils import timezone
from utils.cuid import CUID_ATTENDEE
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

    def time_out(self) -> None:
        self.end_at = timezone.now()

    def __str__(self) -> str:
        return (
            f"Attendee: {self.user.last_name} at Room: {self.attendance.room.name}"
        )
