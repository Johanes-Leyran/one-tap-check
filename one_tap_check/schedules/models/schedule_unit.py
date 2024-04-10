from django.db import models
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from utils.cuid import CUID_SCHEDULE_UNIT


class ScheduleUnit(TimezoneAwareMixin):
    cuid2 = models.CharField(
        default=CUID_SCHEDULE_UNIT.generate,
        max_length=CUID_SCHEDULE_UNIT.length,
        primary_key=True,
        editable=False,
        unique=True
    )
    schedule = models.ForeignKey(
        'schedules.ScheduleSheet',
        on_delete=models.CASCADE
    )
    rooms = models.ForeignKey(
        'rooms.Room',
        on_delete=models.SET_NULL,
        null=True
    )
    teacher = models.ForeignKey(
        'profiles.SHSTeacherProfile',
        on_delete=models.SET_NULL,
        related_query_name='teacher',
        null=True
    )
    DAYS_CHOICES = [
        ('M', 'Monday'),
        ('Tu', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('Sa', 'Saturday'),
        ('Su', 'Sunday')
    ]
    at_day = models.CharField(
        max_length=9,
        choices=DAYS_CHOICES,
        verbose_name="Day of the schedule"
    )
    subject = models.ForeignKey(
        'profiles.Subject',
        verbose_name="Subject of the schedule unit",
        on_delete=models.SET_NULL,
        null=True
    )
    section = models.ForeignKey(
        'profiles.Section',
        on_delete=models.SET_NULL,
        null=True
    )
    starting_at = models.DateTimeField()
    end_at = models.DateTimeField()
