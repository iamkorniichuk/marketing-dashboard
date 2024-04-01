from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "Active", "Active"
    REMOVAL_PLANNED = "Removal Planned", "Removal Planned"


class Region(models.Model):
    class Meta:
        ordering = ["name"]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    canonical_name = models.CharField(max_length=128)
    country_code = models.CharField(max_length=32)
    status = models.CharField(max_length=128, choices=StatusChoices.choices)

    def __str__(self):
        return self.name
