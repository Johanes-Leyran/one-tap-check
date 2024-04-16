from django.contrib import admin
from .models.attendance import Attendance
from .models.attendee import Attendee


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


# Register your models here.
admin.site.register(Attendance, ShowPKAdmin)
admin.site.register(Attendee, ShowPKAdmin)
