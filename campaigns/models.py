from django.db import models


class CrossroadsToTiktokBusinessIdentifiers(models.Model):
    class Meta:
        verbose_name_plural = "Crossroads To Tiktok Business Identifiers"

    tiktok_business = models.CharField(max_length=128, unique=True)
    crossroads = models.CharField(max_length=128, unique=True)


class CrossroadsCampaign(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class TiktokBusinessAdvertiser(models.Model):
    id = models.CharField(max_length=128, primary_key=True)


class TiktokBusinessCampaign(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)
    advertiser = models.ForeignKey(TiktokBusinessAdvertiser, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name
