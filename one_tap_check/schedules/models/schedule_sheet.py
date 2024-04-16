from django.db import models
from utils.cuid import CUID_SCHEDULE


class ScheduleSheet(models.Model):
    cuid2 = models.CharField(
        default=CUID_SCHEDULE.generate,
        max_length=CUID_SCHEDULE.length,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'Schedule {self.name}'
