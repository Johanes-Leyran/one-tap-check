from django.db import models
from django.contrib.auth import get_user_model
from mixins.timeawarezonemixin import TimezoneAwareMixin
from rooms.models import Room
from utils.cuid import CUID_SCHEDULE, CUID_SCHEDULE_UNIT


class ScheduleSheet(TimezoneAwareMixin):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    name = models.CharField(max_length=120)
    starting_at = models.DateField()
    end_at = models.DateField()


class ScheduleUnit(TimezoneAwareMixin):
    schedule = models.ForeignKey(
        ScheduleSheet,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=120)
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True
    )
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_query_name='teacher',
        null=True
    )
    starting_at = models.DateTimeField()
    end_at = models.DateTimeField()
        
    DAYS_CHOICES = [
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
        ('Su', 'Sunday')
    ]
    
    at_day = models.CharField(
        max_length=9,
        choices=DAYS_CHOICES,
        verbose_name="Day"
    )
       