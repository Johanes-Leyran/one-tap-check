from django.db import models
from django.contrib.auth import get_user_model
from utils.cuid import CUID_TAG


class Tag(models.Model):
    cuid2 = models.CharField(
        default=CUID_TAG.generate,
        max_length=CUID_TAG.length,
        primary_key=True,
        editable=False,
        unique=True
    )
    is_compromised = models.BooleanField(
        default=False,
        verbose_name="If the tag is compromised or not"
    )
    user = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.SET_NULL,
        related_name='tags'
    )

    def __str__(self):
        return f'Tag of {self.user.last_name}'
