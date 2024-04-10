from django.db import models
# todo validate data


class Department(models.Model):
    department_name = models.CharField(
        max_length=120,
    )

