from django.db import models

from regions.models import Region
from campaigns.models import TiktokAdvertiser


class TiktokAd(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    advertiser = models.ForeignKey(TiktokAdvertiser, models.PROTECT, related_name="ads")
    first_shown = models.DateField()
    last_shown = models.DateField()
    paid_for = models.CharField(max_length=128)
    total_viewers = models.PositiveIntegerField()
    unique_viewers = models.PositiveIntegerField()

    def get_absolute_url(self):
        return f"https://library.tiktok.com/ads/detail/?ad_id={self.id}"


class RegionAge(models.Model):
    region = models.ForeignKey(Region, models.PROTECT)
    min_age = models.PositiveSmallIntegerField()
    max_age = models.PositiveSmallIntegerField()
    ad = models.ForeignKey(TiktokAd, models.CASCADE, related_name="ages")


class RegionGender(models.Model):
    region = models.ForeignKey(Region, models.PROTECT)
    is_male = models.BooleanField()
    is_female = models.BooleanField()
    is_unknown = models.BooleanField()
    ad = models.ForeignKey(TiktokAd, models.CASCADE, related_name="genders")


class RegionViewers(models.Model):
    region = models.ForeignKey(Region, models.PROTECT)
    unique_viewers = models.PositiveIntegerField()
    ad = models.ForeignKey(TiktokAd, models.CASCADE, related_name="viewers")
