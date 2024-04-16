from .models.schedule_sheet import ScheduleSheet
from django.contrib.auth import get_user_model
from django.db.models import DateTimeField
from django.utils import timezone
import calendar

"""
    find the right section and subject when 
    the attendance is created
"""


def get_nearest_schedule(teacher: get_user_model(), date_time: DateTimeField):
    # could be none
    schedule = teacher.schedule
    current_time = timezone.localtime(timezone.now().replace(second=0, microsecond=0))
    current_day = calendar.day_name[current_time.weekday()]

    # get all the schedule within that day
    current_day_schedule_unit = ScheduleSheet.objects.get(pk=schedule.pk)
    current_day_schedule_unit = current_day_schedule_unit.schedule_units.filter(at_day=current_day)

    nearest_schedule_unit = None
    lowest_time_difference = None

    # find the nearest
    for schedule_unit in current_day_schedule_unit:
        difference = abs(schedule_unit.starting_at - current_time).total_seconds()

        if lowest_time_difference is None or lowest_time_difference > difference:
            lowest_time_difference = difference
            nearest_schedule_unit = schedule_unit

    return nearest_schedule_unit
