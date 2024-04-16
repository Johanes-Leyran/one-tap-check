from django.contrib import admin
from .models.schedule_unit import ScheduleUnit
from .models.schedule_sheet import ScheduleSheet
# Register your models here.

admin.site.register(ScheduleSheet)
admin.site.register(ScheduleUnit)
