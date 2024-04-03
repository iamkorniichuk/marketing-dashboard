from datetime import datetime, timedelta
from typing import Iterable
from django.db.models import QuerySet

from keywords.models import Keyword
from metrics.models import GoogleAdsForecastKeywordMetrics
from regions.models import Region

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


def generate_forecast_metrics(
    queryset: QuerySet[Keyword],
    regions: Iterable[Region],
    start_date=None,
    end_date=None,
) -> Iterable[GoogleAdsForecastKeywordMetrics]:
    if not start_date:
        start_date = datetime.now() + timedelta(days=1)

    if not end_date:
        end_date = start_date + timedelta(weeks=2)

    keywords = queryset.values_list("text", flat=True)
    region_ids = [obj.id for obj in regions]

    data = api_client.request_forecast_keywords_metrics(
        keywords,
        region_ids,
        start_date,
        end_date,
    )

    results = []
    for row in data:
        exact_keywords = queryset.filter(text__iexact=row["keyword"])

        obj, _ = GoogleAdsForecastKeywordMetrics.objects.update_or_create(
            keyword=exact_keywords.first(),
            start_date=row["start_date"],
            end_date=row["end_date"],
            defaults={
                "impressions": row["impressions"],
                "partners_impressions": row["impressions_partners"],
                "ctr": row["ctr"],
                "partners_ctr": row["ctr_partners"],
                "average_cpc": row["avg_cpc"],
                "partners_average_cpc": row["avg_cpc_partners"],
                "clicks": row["clicks"],
                "partners_clicks": row["clicks_partners"],
                "cost": row["cost"],
                "partners_cost": row["cost_partners"],
                "conversions": row["conversions"],
                "partners_conversions": row["conversions_partners"],
                "conversion_rate": row["conversion_rate"],
                "partners_conversion_rate": row["conversion_rate_partners"],
                "average_cpa": row["avg_cpa"],
                "partners_average_cpa": row["avg_cpa_partners"],
            },
        )

        obj.regions.set(regions)
        results.append(obj)

    return results
