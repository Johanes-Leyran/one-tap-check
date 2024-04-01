from django.db import models
from django.core.validators import MinValueValidator
from utils.cuid import CUID_ROOM, CUID_SCANNER
from simple_history.models import HistoricalRecords


class Building(models.Model):
    name = models.CharField(max_length=128)
    history = HistoricalRecords()
    
    def __str__(self):
        return f'Building: {self.name}'


class Scanner(models.Model):
    cuid2 = models.CharField(
        primary_key=True,
        default=CUID_SCANNER.generate,
        max_length=CUID_SCANNER.length,
        editable=False,
        unique=True
    )
    STATUS_CHOICE = (
        ("WORKING", "Working"),
        ("NOT WORKING", "Not Working"),
        ("BARELY WORKING", "Barely Working")
    )
    status = models.CharField(
        choices=STATUS_CHOICE,
        max_length=14
    )
    is_active = models.BooleanField(default=True)


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
    )
    scanner = models.OneToOneField(
        Scanner,
        verbose_name="Scanner designated to the room",
        on_delete=models.PROTECT,
        related_name="designated_room"
    )
    name = models.CharField(max_length=128)
    is_available = models.BooleanField(default=True)
    description = models.TextField(verbose_name="The description of the room")
    at_floor = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    
    def __str__(self) -> str:
        return (
            f'Room: {self.name} at Building: {self.building.name}'
        )
