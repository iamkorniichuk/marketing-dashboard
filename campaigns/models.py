from django.db import models


class CrossroadsCampaign(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "date"],
                name="crossroads_unique_id_for_date",
            )
        ]

    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    date = models.DateField()
    revenue = models.FloatField()
    rpc = models.FloatField()
    rpv = models.FloatField()
    total_visitors = models.IntegerField()
    filtered_visitors = models.IntegerField()
    lander_visitors = models.IntegerField()
    lander_searches = models.IntegerField()
    revenue_events = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class TiktokBusinessCampaign(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identifier", "date"],
                name="tiktok_business_unique_id_for_date",
            )
        ]

    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    advertiser_id = models.CharField(max_length=128)
    date = models.DateField()
    video_play_actions = models.IntegerField()
    video_watched_2s = models.IntegerField()
    video_watched_6s = models.IntegerField()
    video_views_p25 = models.IntegerField()
    video_views_p50 = models.IntegerField()
    video_views_p75 = models.IntegerField()
    video_views_p100 = models.IntegerField()
    cost_per_conversion = models.FloatField()
    cpc = models.FloatField()
    ctr = models.FloatField()
    clicks = models.IntegerField()
    spend = models.FloatField()
    conversion = models.FloatField()

    def __str__(self) -> str:
        return self.name


class MergedCampaign(models.Model):

    tiktok_business = models.ForeignKey(
        TiktokBusinessCampaign,
        on_delete=models.CASCADE,
    )
    crossroads = models.ForeignKey(
        CrossroadsCampaign,
        on_delete=models.CASCADE,
    )
