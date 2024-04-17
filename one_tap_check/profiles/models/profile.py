from django.db import models
from django.contrib.auth import get_user_model
from attendances.models.attendee import Attendee
# Todo: add logging system
# Todo: add validation on models
# Todo: study absolute urls and urls best practices
# Todo: study about on delete

# Since profile are dependent to user they must be cascade


class SHSStudentProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="Account connected to the profile",
        on_delete=models.CASCADE,
        null=True,
        related_name="student_profile"
    )
    student_number = models.CharField(
        max_length=120,
        blank=True
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

    def count_on_time(self):
        return Attendee.objects.filter(user=self.account, status='On Time').count()

    def count_absent_time(self):
        return Attendee.objects.filter(user=self.account, status='Absent').count()

    def count_late_time(self):
        return Attendee.objects.filter(user=self.account, status='Late').count()

    def __str__(self):
        return f'Student Profile: {self.account.last_name}'


class SHSTeacherProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(),
        verbose_name="Account connected to the profile",
        on_delete=models.CASCADE,
        null=True,
        related_name="teacher_profile"
    )
    teacher_number = models.CharField(
        max_length=120,
        blank=True
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
        on_delete=models.CASCADE,
        null=True,
        related_name="staff_profile"
    )
    staff_number = models.CharField(
        max_length=120,
        blank=True
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
