from django.contrib import admin
from .models.attendance import Attendance
from .models.attendee import Attendee

# Register your models here.
admin.site.register(Attendance)
admin.site.register(Attendee)
