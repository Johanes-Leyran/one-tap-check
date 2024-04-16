from django.contrib import admin
from .models.profile import StaffProfile, SHSTeacherProfile, SHSStudentProfile
from .models.section import Section
from .models.subject import Subject
from .models.department import Department

admin.site.register(StaffProfile)
admin.site.register(SHSTeacherProfile)
admin.site.register(SHSStudentProfile)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(Department)
