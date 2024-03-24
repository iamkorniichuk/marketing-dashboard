from datetime import datetime, timedelta
from django.contrib import admin

from metrics.models import GoogleAdsForecastKeywordMetrics

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


@admin.action(description="Request forecast metrics")
def request_forecast_metrics(modeladmin, request, queryset):
    regions_keyword = {}
    for obj in queryset.all():
        regions = tuple(obj.regions.values_list("id", flat=True))
        try:
            regions_keyword[regions].append(obj.text)
        except KeyError:
            regions_keyword[regions] = [obj.text]

    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(weeks=2)
    data = []
    for regions, keywords in regions_keyword.items():
        response = api_client.request_forecast_keywords_metrics(
            keywords,
            regions,
            start_date,
            end_date,
        )
        data.extend(response)

    metrics = []
    for row in data:
        keyword = queryset.filter(text__iexact=row["keyword"])
        for region_id in row["region_ids"]:
            keyword = keyword.filter(regions__id=region_id)

        metrics.append(
            GoogleAdsForecastKeywordMetrics(
                keyword=keyword.first(),
                start_date=row["start_date"],
                end_date=row["end_date"],
                impressions=row["impressions"],
                partners_impressions=row["impressions_partners"],
                ctr=row["ctr"],
                partners_ctr=row["ctr_partners"],
                average_cpc=row["avg_cpc"],
                partners_average_cpc=row["avg_cpc_partners"],
                clicks=row["clicks"],
                partners_clicks=row["clicks_partners"],
                cost=row["cost"],
                partners_cost=row["cost_partners"],
                conversions=row["conversions"],
                partners_conversions=row["conversions_partners"],
                conversion_rate=row["conversion_rate"],
                partners_conversion_rate=row["conversion_rate_partners"],
                average_cpa=row["avg_cpa"],
                partners_average_cpa=row["avg_cpa_partners"],
            )
        )
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
