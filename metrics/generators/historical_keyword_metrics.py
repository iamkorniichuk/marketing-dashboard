from datetime import datetime
from typing import Iterable
from django.db.models import QuerySet
from commons.models import filter_contains_all

from keywords.models import GoogleAdsKeyword
from keywords.utils import extract_regions_groups
from metrics.models import GoogleAdsHistoricalKeywordMetrics

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


def generate_historical_metrics(
    queryset: QuerySet[GoogleAdsKeyword],
) -> Iterable[GoogleAdsHistoricalKeywordMetrics]:
    regions_groups = extract_regions_groups(queryset)

    data = []
    for regions, keywords in regions_groups.items():
        response = api_client.request_historical_keywords_metrics(keywords, regions)
        data.extend(response)

    today = datetime.now()
    metrics = []
    for row in data:
        exact_keywords = queryset.filter(text__iexact=row["keyword"])
        keyword = filter_contains_all(exact_keywords, regions=row["region_ids"])

        metrics.append(
            GoogleAdsHistoricalKeywordMetrics(
                keyword=keyword.first(),
                date=today.now(),
                average_month_search=row["avg_month_search"],
                partners_average_month_search=row["avg_month_search_partners"],
                average_cpc=row["avg_cpc"],
                partners_average_cpc=row["avg_cpc_partners"],
                low_page_bid=row["low_page_bid"],
                partners_low_page_bid=row["low_page_bid_partners"],
                high_page_bid=row["high_page_bid"],
                partners_high_page_bid=row["high_page_bid_partners"],
            )
        )

    return metrics
