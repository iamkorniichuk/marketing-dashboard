from datetime import datetime, timedelta
from typing import Iterable
from django.db.models import QuerySet
from commons.models import filter_contains_all

from keywords.models import GoogleAdsKeyword
from keywords.utils import extract_regions_groups
from metrics.models import GoogleAdsForecastKeywordMetrics

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


def generate_forecast_metrics(
    queryset: QuerySet[GoogleAdsKeyword],
    start_date=None,
    end_date=None,
) -> Iterable[GoogleAdsForecastKeywordMetrics]:
    if not start_date:
        start_date = datetime.now() + timedelta(days=1)

    if not end_date:
        end_date = start_date + timedelta(weeks=2)

    regions_groups = extract_regions_groups(queryset)

    data = []
    for regions, keywords in regions_groups.items():
        response = api_client.request_forecast_keywords_metrics(
            keywords,
            regions,
            start_date,
            end_date,
        )
        data.extend(response)

    metrics = []
    for row in data:
        exact_keywords = queryset.filter(text__iexact=row["keyword"])
        keyword = filter_contains_all(exact_keywords, regions=row["region_ids"])

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

    return metrics
