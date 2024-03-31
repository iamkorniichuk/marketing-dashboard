from datetime import datetime
from typing import Iterable
from django.db.models import QuerySet

from keywords.models import Keyword
from metrics.models import GoogleAdsHistoricalKeywordMetrics
from regions.models import Region

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


def generate_historical_metrics(
    queryset: QuerySet[Keyword],
    regions: Iterable[Region],
) -> Iterable[GoogleAdsHistoricalKeywordMetrics]:
    keywords = queryset.values_list("text", flat=True)
    region_ids = [obj.id for obj in regions]

    data = []
    data = api_client.request_historical_keywords_metrics(keywords, region_ids)

    today = datetime.now()
    for row in data:
        exact_keywords = queryset.filter(text__iexact=row["keyword"])

        obj, _ = GoogleAdsHistoricalKeywordMetrics.objects.update_or_create(
            keyword=exact_keywords.first(),
            date=today.now(),
            defaults={
                "average_month_search": row["avg_month_search"],
                "partners_average_month_search": row["avg_month_search_partners"],
                "average_cpc": row["avg_cpc"],
                "partners_average_cpc": row["avg_cpc_partners"],
                "low_page_bid": row["low_page_bid"],
                "partners_low_page_bid": row["low_page_bid_partners"],
                "high_page_bid": row["high_page_bid"],
                "partners_high_page_bid": row["high_page_bid_partners"],
            },
        )
        obj.regions.set(regions)
