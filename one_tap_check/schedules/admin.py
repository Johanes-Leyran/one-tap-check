from django.contrib import admin
from .models.schedule_unit import ScheduleUnit
from .models.schedule_sheet import ScheduleSheet
# Register your models here.


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


admin.site.register(ScheduleSheet, ShowPKAdmin)
admin.site.register(ScheduleUnit, ShowPKAdmin)
