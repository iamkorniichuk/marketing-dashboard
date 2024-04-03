from django.db import models

from campaigns.models import CrossroadsCampaign
from keywords.models import Keyword
from regions.models import Region


class CrossroadsKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["campaign", "lander_keyword", "date"],
                name="unique_crossroads_keywords_metrics_for_date",
            )
        ]
        verbose_name = "Crossroads Keyword's"
        verbose_name_plural = "Crossroads Keywords'"

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
        verbose_name = "Historical Keyword's"
        verbose_name_plural = "Historical Keywords'"

    keyword = models.ForeignKey(
        Keyword,
        on_delete=models.PROTECT,
        related_name="historical_metrics",
    )
    regions = models.ManyToManyField(Region, related_name="historical_metrics")
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
        verbose_name = "Forecast Keyword's"
        verbose_name_plural = "Forecast Keywords'"

    keyword = models.ForeignKey(
        Keyword,
        on_delete=models.PROTECT,
        related_name="forecast_metrics",
    )
    regions = models.ManyToManyField(Region, related_name="forecast_metrics")
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


class GoogleSearchKeywordMetrics(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["keyword", "date", "region"],
                name="unique_google_search_keyword_metrics_for_date_and_region",
            )
        ]
        verbose_name = "Competition Keyword's"
        verbose_name_plural = "Competition Keywords'"

    keyword = models.ForeignKey(Keyword, on_delete=models.PROTECT)
    date = models.DateField()
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="search_metrics"
    )
    competition = models.FloatField()
    average_cpc = models.FloatField(verbose_name="avg cpc")
    partners_average_cpc = models.FloatField(verbose_name="part. avg cpc")
    low_page_bid = models.FloatField()
    partners_low_page_bid = models.FloatField(verbose_name="part. low page bid")
    high_page_bid = models.FloatField()
    partners_high_page_bid = models.FloatField(verbose_name="part. high page bid")
    volume_trends_image = models.ImageField(upload_to="volume_trends/")
