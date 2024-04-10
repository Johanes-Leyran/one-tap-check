from django.db import models
from django.contrib.auth import get_user_model
from mixins.time_awarezone_mixin import TimezoneAwareMixin
from utils.cuid import CUID_SCHEDULE


class ScheduleSheet(TimezoneAwareMixin):
    cuid2 = models.CharField(
        default=CUID_SCHEDULE.generate,
        max_length=CUID_SCHEDULE.length,
        primary_key=True,
        editable=False,
        unique=True
    )
    users = models.ManyToManyField(
        get_user_model(),
        related_name="schedules"
    )
    name = models.CharField(max_length=120)
    """
        starting_at: the start where this schedule will be implemented

        end_at: the end of the schedule implementation
    """
    starting_at = models.DateField()
    end_at = models.DateField()
