from django.db import models
from django.contrib.auth import get_user_model


class BaseProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name="User connected to the profile",
        related_name="profile",
        on_delete=models.SET_NULL, 
        null=True
    )
     
    class Meta:
        abstract = True


class StudentProfile(BaseProfile):
    section = models.CharField(
        "Section of the student",
        max_length=60,
    )
    adviser = models.ForeignKey(
        get_user_model(),
        verbose_name="Adviser of the student",
        related_name="advisory_students",
    )
    GRADES_CHOICES = {
        "11": "Grade 11",
        "12": "Grade 12"
    }
    grade = models.Model(
        choices=GRADES_CHOICES,
        max_length=3,
    )
    
    def clean(self):
        pass
        # TODO:think of a way to validate the adviser 
    
    
    