from django.db import models
from django.core.validators import MinValueValidator
from utils.cuid import CUID_ROOM


class Building(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return f'Building: {self.name}'


class Room(models.Model):
    cuid2 = models.CharField(
        primary_key=True,
        default=CUID_ROOM.generate,
        max_length=CUID_ROOM.length,
        editable=False,
        unique=True
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.PROTECT,
        related_name='rooms',
        related_query_name='building'
    )
    name = models.CharField(max_length=128)
    is_available = models.BooleanField(default=True)
    at_floor = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self) -> str:
        return (
            f'Room: {self.name} at Building: {self.building.name}'
        )
    