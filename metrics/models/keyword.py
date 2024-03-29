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
    average_month_search = models.FloatField(verbose_name="avg month search")
    partners_average_month_search = models.FloatField(
        verbose_name="part. avg month search"
    )
    average_cpc = models.FloatField(verbose_name="avg cpc")
    partners_average_cpc = models.FloatField(verbose_name="part. avg cpc")
    low_page_bid = models.FloatField()
    partners_low_page_bid = models.FloatField(verbose_name="part. low page bid")
    high_page_bid = models.FloatField()
    partners_high_page_bid = models.FloatField(verbose_name="part. high page bid")


class GoogleAdsForecastKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["keyword", "start_date", "end_date"],
                name="unique_google_ads_forecast_keyword_metrics_for_date",
            )
        ]
        verbose_name_plural = "Google Ads Forecast Keyword Metrics"

    keyword = models.ForeignKey(
        GoogleAdsKeyword,
        on_delete=models.PROTECT,
        related_name="forecast_metrics",
    )
    start_date = models.DateField(verbose_name="start")
    end_date = models.DateField(verbose_name="end")
    impressions = models.FloatField(verbose_name="impres.")
    partners_impressions = models.FloatField(verbose_name="part. impres.")
    ctr = models.FloatField()
    partners_ctr = models.FloatField(verbose_name="part. ctr")
    average_cpc = models.FloatField(verbose_name="avg cpc")
    partners_average_cpc = models.FloatField(verbose_name="part. avg cpc")
    clicks = models.FloatField()
    partners_clicks = models.FloatField(verbose_name="part. clicks")
    cost = models.FloatField()
    partners_cost = models.FloatField(verbose_name="part. cost")
    conversions = models.FloatField(verbose_name="convers.")
    partners_conversions = models.FloatField(verbose_name="part. convers.")
    conversion_rate = models.FloatField(verbose_name="convers. rate")
    partners_conversion_rate = models.FloatField(verbose_name="part. convers. rate")
    average_cpa = models.FloatField(verbose_name="avg cpa")
    partners_average_cpa = models.FloatField(verbose_name="part. avg cpa")
