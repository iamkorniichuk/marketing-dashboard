from django.contrib import admin

from metrics.models import (
    GoogleAdsForecastKeywordMetrics,
    GoogleAdsHistoricalKeywordMetrics,
)
from metrics.generators import generate_forecast_metrics, generate_historical_metrics

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


@admin.action(description="Request forecast metrics")
def request_forecast_metrics(modeladmin, request, queryset):
    metrics = generate_forecast_metrics(queryset)

    GoogleAdsForecastKeywordMetrics.objects.bulk_create(
        metrics,
        update_conflicts=True,
        unique_fields=["keyword", "start_date", "end_date"],
        update_fields=[
            "impressions",
            "partners_impressions",
            "ctr",
            "partners_ctr",
            "average_cpc",
            "partners_average_cpc",
            "clicks",
            "partners_clicks",
            "cost",
            "partners_cost",
            "conversions",
            "partners_conversions",
            "conversion_rate",
            "partners_conversion_rate",
            "average_cpa",
            "partners_average_cpa",
        ],
    )


@admin.action(description="Request historical metrics")
def request_historical_metrics(modeladmin, request, queryset):
    metrics = generate_historical_metrics(queryset)

    GoogleAdsHistoricalKeywordMetrics.objects.bulk_create(
        metrics,
        update_conflicts=True,
        unique_fields=["keyword", "date"],
        update_fields=[
            "average_month_search",
            "partners_average_month_search",
            "average_cpc",
            "partners_average_cpc",
            "low_page_bid",
            "partners_low_page_bid",
            "high_page_bid",
            "partners_high_page_bid",
        ],
    )
