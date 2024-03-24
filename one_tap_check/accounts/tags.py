from django.db import models
from utils.cuid import CUID_TAG
from django.contrib.auth import get_user_model


class Tag(models.Model):
    cuid2 = models.CharField(
        verbose_name="Cuid2 of the tag",
        default=CUID_TAG.generate,
        max_length=CUID_TAG.length,
        editable=False,
        unique=True,
        primary_key=True
    )
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        verbose_name="The account connected to the tag"
    )
    is_compromise = models.BooleanField(
        verbose_name=(
            """ 
            If the tag is stolen, missing, 
            or any scenario where the user 
            has no access to the tag. 
            """
        ),
        default=False
    )

