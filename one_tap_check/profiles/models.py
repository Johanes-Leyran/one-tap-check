from django.db import models
from django.contrib.auth import get_user_model
# Todo: add logging system
# Todo: add validation on models
# Todo: study absolute urls and urls best practices
# Todo: study about on delete


class BaseProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="User of to the profile",
        on_delete=models.SET_NULL,
        null=True
    )

    def get_username(self):
        if self.account:
            return (
                f"{self.account.last_name}, {self.account.first_name}"
            )
        return False

    # Todo: add logs field

    class Meta:
        abstract = True


class SHSStudentProfile(BaseProfile):
    adviser = models.ForeignKey(
        get_user_model(),
        verbose_name="Adviser of the student",
        related_name="advisory_students",
        on_delete=models.SET_NULL,
        null=True,
    )
    GRADE_CHOICES = (
        ('11', 'Grade 11'),
        ('12', 'Grade 12')
    )
    grade = models.CharField(
        verbose_name='Grade of the Student',
        max_length=2,
        choices=GRADE_CHOICES
    )
    section = models.CharField(
        verbose_name='Section of the Student',
        max_length=30
    )


class SHSTeacherProfile(BaseProfile):
    department = models.CharField(
        verbose_name='Department of the Teacher',
        max_length=120,
    )

    # Todo: add more fields for the teacher model

    def get_advisory_students(self):
        return SHSStudentProfile.objects.filter(adviser=self.account)
