from django.db import models

from campaigns.models import CrossroadsCampaign
from keywords.models import GoogleAdsKeyword


class CrossroadsKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "lander_keyword", "date"],
                name="unique_crossroads_keywords_metrics_for_date",
            )
        ]
        verbose_name_plural = "Crossroads Keyword Metrics"

    campaign = models.ForeignKey(
        CrossroadsCampaign,
        on_delete=models.PROTECT,
        related_name="keyword_metrics",
    )
    lander_keyword = models.CharField(max_length=128)
    clicks = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.lander_keyword


class GoogleAdsHistoricalKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["keyword", "date"],
                name="unique_google_ads_historical_keyword_metrics_for_date",
            )
        ]
        verbose_name_plural = "Google Ads Historical Keyword Metrics"

    keyword = models.ForeignKey(
        GoogleAdsKeyword,
        on_delete=models.PROTECT,
        related_name="historical_metrics",
    )
    date = models.DateField()
    average_month_search = models.FloatField()
    partners_average_month_search = models.FloatField()
    average_cpc = models.FloatField()
    partners_average_cpc = models.FloatField()
    low_page_bid = models.FloatField()
    partners_low_page_bid = models.FloatField()
    high_page_bid = models.FloatField()
    partners_high_page_bid = models.FloatField()
