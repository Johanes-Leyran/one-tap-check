from django.db import models
from rooms.models import Room
from django.contrib.auth import get_user_model
from mixins.TimezoneAwareMixin import TimezoneAwareMixin
from django.utils import timezone
# Todo: make this more easy to read and adjust


class Attendance(TimezoneAwareMixin):
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
    end_at = models.DateField(null=True)
    
    def __str__(self):
        return (
            f"Attendance of Teacher: {self.teacher.name} at Room: {self.room.name}"
        )


class Attendee(TimezoneAwareMixin):
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
    starting_at = models.DateTimeField(default=timezone.now)  # time in
    end_at = models.DateTimeField(null=True)  # time out
    
    def __str__(self):
        return (
            f"Attendee: {self.user.last_name} at Room: {self.attendance.room.name}"
        )
