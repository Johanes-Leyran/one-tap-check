from django.db import models
from django.utils.


class ProfilePKGeneratorMixin(models.Model):

    def generate_id_length(self) -> [str, int]:
        result_id = f"pf-{self.account.pk[-10:]}"
        return result_id, 10

# generate id and returns the length of the id

    class Meta:
        abstract = True
