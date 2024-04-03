from django.db import models


class CrossroadsCampaign(models.Model):
    class Meta:
        verbose_name = "Crossroads Campaign"
        verbose_name_plural = "Crossroads"

    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class TiktokBusinessAdvertiser(models.Model):
    id = models.CharField(max_length=128, primary_key=True)


class TiktokBusinessCampaign(models.Model):
    class Meta:
        verbose_name = "Tiktok Business Campaign"
        verbose_name_plural = "Tiktok Business"

    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256)
    advertiser = models.ForeignKey(
        TiktokBusinessAdvertiser,
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
