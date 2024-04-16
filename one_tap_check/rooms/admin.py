from django.contrib import admin
from .models.room import Room, Building
from .models.scanner import Scanner
# Register your models here.

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Scanner)
