from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rooms.models import Room


class TimezoneAwareMixin(models.Model):
    def clean(self):
        if self.starting_at >= self.end_at:
            raise ValidationError("starting date must not be ahead of end date")
    
    def save(self, *args, **kwargs):
        if not self.starting_at.tzinfo:
            self.starting_at = timezone.make_aware(self.starting_at)
        
        if not self.end_at.tzinfo and not self.end_at:
            self.end_at = timezone.make_aware(self.end_at)
            
        super().save(*args, **kwargs)
        
    class Meta:
        abstract = True


class ScheduleSheet(TimezoneAwareMixin):
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    starting_at = models.DateField()
    end_at = models.DateField()


class ScheduleRoom(TimezoneAwareMixin):
    schedule = models.ForeignKey(ScheduleSheet, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, related_query_name='teacher', null=True
    )
    starting_at = models.DateTimeField()
    end_at = models.DateTimeField()
        
    DAYS_CHOICES = [
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('Th', 'Thursday'),
        ('F', 'Friday'),
        ('S', 'Saturday'),
        ('Su', 'Sunday')
    ]
    
    at_day = models.CharField(max_length=9, choices=DAYS_CHOICES, verbose_name="Day")
       