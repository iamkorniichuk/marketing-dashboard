from django.db import models


class CrossroadsCampaign(models.Model):
    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    updated = models.DateTimeField(auto_now=True)
    revenue = models.FloatField()
    rpc = models.FloatField()
    rpv = models.FloatField()
    total_visitors = models.IntegerField()
    filtered_visitors = models.IntegerField()
    lander_visitors = models.IntegerField()
    lander_searches = models.IntegerField()
    revenue_events = models.IntegerField()


class TiktokBusinessCampaign(models.Model):
    identifier = models.CharField(max_length=128)
    name = models.IntegerField()
    advertiser_id = models.CharField(max_length=128)
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
