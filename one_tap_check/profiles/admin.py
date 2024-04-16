from django.contrib import admin
from .models.profile import StaffProfile, SHSTeacherProfile, SHSStudentProfile
from .models.section import Section
from .models.subject import Subject
from .models.department import Department


class ShowPKAdmin(admin.ModelAdmin):
    readonly_fields = ('pk',)


admin.site.register(StaffProfile, ShowPKAdmin)
admin.site.register(SHSTeacherProfile, ShowPKAdmin)
admin.site.register(SHSStudentProfile, ShowPKAdmin)
admin.site.register(Subject, ShowPKAdmin)
admin.site.register(Section, ShowPKAdmin)
admin.site.register(Department, ShowPKAdmin)
