from django.db import models
from django.contrib.auth import get_user_model
# Todo: add logging system
# Todo: add validation on models
# Todo: study absolute urls and urls best practices
# Todo: study about on delete


class SHSStudentProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="Account connected to the profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_profile"
    )
    advisor = models.ForeignKey(
        'profiles.SHSTeacherProfile',
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
    section = models.ForeignKey(
        'profiles.Section',
        on_delete=models.SET_NULL,
        related_name='students',
        null=True
    )

    def __str__(self):
        return f'Student Profile: {self.account.last_name}'


class SHSTeacherProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="Account connected to the profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="teacher_profile"
    )
    department = models.ForeignKey(
        'profiles.Department',
        verbose_name='Department of the Teacher',
        on_delete=models.SET_NULL,
        null=True
    )
    advisory_section = models.OneToOneField(
        'profiles.Section',
        on_delete=models.SET_NULL,
        related_name='advisor',
        null=True,
        blank=True
    )
    sections = models.ManyToManyField(
        'profiles.Section',
        related_name='teacher_profiles',
        blank=True
    )
    subject = models.ManyToManyField(
        'profiles.Subject',
        related_name='teachers',
        blank=True
    )

    def __str__(self):
        return f'Teacher Profile: {self.account.last_name}'


class StaffProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="Account connected to the profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="staff_profile"
    )
    role = models.CharField(
        verbose_name="Role of the Staff",
        max_length=120
    )
    department = models.ForeignKey(
        'profiles.Department',
        verbose_name='Department of the Staff',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Staff Profile: {self.account.last_name}'
