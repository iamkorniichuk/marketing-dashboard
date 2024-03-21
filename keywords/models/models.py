from django.db import models

from regions.models import Region


class GoogleAdsKeyword(models.Model):
    text = models.CharField(max_length=256)
    regions = models.ManyToManyField(Region, related_name="keywords")

    def __str__(self):
        return self.text
