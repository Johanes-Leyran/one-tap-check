from django.db import models
# todo validate data


class Department(models.Model):
    department_name = models.CharField(
        max_length=120,
    )

    def __str__(self):
        return self.department_name

