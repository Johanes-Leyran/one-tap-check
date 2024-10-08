from django.contrib import admin
from .models.profile import StaffProfile, SHSTeacherProfile, SHSStudentProfile
from .models.section import Section
from .models.subject import Subject
from .models.department import Department


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


admin.site.register(StaffProfile)
admin.site.register(SHSTeacherProfile)
admin.site.register(SHSStudentProfile)
admin.site.register(Subject, ShowPKAdmin)
admin.site.register(Section, ShowPKAdmin)
admin.site.register(Department, ShowPKAdmin)
