from django.db import models
from django.contrib.auth import get_user_model


class BaseProfile:
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL)
    
    class Meta:
        abstract = True
    
    
class ScheduleMixin:
    schedule = None
    
    class Meta:
        abstract = True
    
    
class StudentProfile(BaseProfile, ScheduleMixin):
    section = models.CharField(max_length=60)
    adviser = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, related_name="advisory_students"
    )
    GRADE_CHOICES = [
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]
    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        default='11',
        verbose_name='Grade'
    )


class TeacherProfile(BaseProfile, ScheduleMixin):
    department = models.CharField(max_length=60)
    

class StaffProfile(BaseProfile, ScheduleMixin):
    role = models.CharField(max_length=120)
    
    