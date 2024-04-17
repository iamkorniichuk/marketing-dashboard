from django.db import models

from regions.models import Region


class CrossroadsCampaign(models.Model):
    class Meta:
        verbose_name = "Crossroads Campaign"
        verbose_name_plural = "Crossroads"

    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class TiktokAdvertiser(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=128, blank=True)
    region = models.ForeignKey(
        Region, models.PROTECT, related_name="tiktok_advertisers", null=True
    )
    total_ads = models.PositiveIntegerField(null=True)

    phone_number = models.CharField(max_length=16, blank=True)
    email = models.EmailField(max_length=254, null=True)
    facebook = models.URLField(max_length=256, null=True)
    youtube = models.URLField(max_length=256, null=True)
    linkedin = models.URLField(max_length=256, null=True)

    def __str__(self):
        return self.name


class TiktokBusinessCampaign(models.Model):
    class Meta:
        verbose_name = "Tiktok Business Campaign"
        verbose_name_plural = "Tiktok Business"

    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)
    advertiser = models.ForeignKey(
        TiktokAdvertiser,
        on_delete=models.PROTECT,
        related_name="campaigns",
    )

    def __str__(self) -> str:
        return self.name


class CrossroadsToTiktokBusinessIdentifiers(models.Model):
    tiktok_business = models.OneToOneField(
        TiktokBusinessCampaign,
        on_delete=models.PROTECT,
        related_name="identifiers",
    )
    crossroads = models.OneToOneField(
        CrossroadsCampaign,
        on_delete=models.PROTECT,
        related_name="identifiers",
    )
