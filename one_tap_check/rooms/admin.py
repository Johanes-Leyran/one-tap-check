from django.contrib import admin
from .models.room import Room, Building
from .models.scanner import Scanner
# Register your models here.


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


admin.site.register(Building, ShowPKAdmin)
admin.site.register(Room, ShowPKAdmin)
admin.site.register(Scanner, ShowPKAdmin)
