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
