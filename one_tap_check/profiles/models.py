from django.db import models
from django.contrib.auth import get_user_model


class BaseProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f'profile of {self.user.lastname}'
    
    
class StudentProfile(BaseProfile):
    section = models.CharField(max_length=60)
    adviser = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, related_name="advisory_students", null=True
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


# class TeacherProfile(BaseProfile):
#     department = models.CharField(max_length=60)
    

class StaffProfile(BaseProfile):
    role = models.CharField(max_length=120)
    department = models.CharField(max_length=60, null=True)
    # add feature to 