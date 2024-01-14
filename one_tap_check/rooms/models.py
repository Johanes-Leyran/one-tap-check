from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Building(models.Model):
    name = models.CharField(max_length=128)
    floors = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f'Building: {self.name}'


class Room(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=128)
    is_available = models.BooleanField(default=True)
    at_floor = models.IntegerField(validators=[MinValueValidator(1)])
    building = models.ForeignKey(
        Building, on_delete=models.PROTECT, related_name='rooms', related_query_name='building'
    )
    
    def __str__(self):
        return f'Room: {self.name} at Building: {self.building.name}'
    