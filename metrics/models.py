from django.db import models

from campaigns.models import CrossroadsCampaign, TiktokBusinessCampaign


class CrossroadsCampaignMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "date"],
                name="crossroads_unique_metrics_for_date",
            )
        ]

    campaign = models.ForeignKey(CrossroadsCampaign, on_delete=models.PROTECT)
    date = models.DateField()
    revenue = models.FloatField()
    rpc = models.FloatField()
    rpv = models.FloatField()
    total_visitors = models.IntegerField()
    filtered_visitors = models.IntegerField()
    lander_visitors = models.IntegerField()
    lander_searches = models.IntegerField()
    revenue_events = models.IntegerField()


class TiktokBusinessCampaignMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "date"],
                name="tiktok_business_unique_metrics_for_date",
            )
        ]

    campaign = models.ForeignKey(TiktokBusinessCampaign, on_delete=models.PROTECT)
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


class CampaignMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tiktok_business_metrics", "crossroads_metrics", "date"],
                name="unique_campaign_metrics_for_date",
            )
        ]

    tiktok_business_metrics = models.ForeignKey(
        TiktokBusinessCampaignMetrics,
        on_delete=models.CASCADE,
    )
    crossroads_metrics = models.ForeignKey(
        CrossroadsCampaignMetrics,
        on_delete=models.CASCADE,
    )
    date = models.DateField()


class CrossroadsKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "lander_keyword", "date"],
                name="unique_crossroads_keywords_metrics_for_date",
            )
        ]

    campaign = models.ForeignKey(CrossroadsCampaign, on_delete=models.PROTECT)
    lander_keyword = models.CharField(max_length=128)
    clicks = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.lander_keyword
