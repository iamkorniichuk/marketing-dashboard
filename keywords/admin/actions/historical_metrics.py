from datetime import datetime
from django.contrib import admin

from metrics.models import GoogleAdsHistoricalKeywordMetrics

from api_clients.google_ads import GoogleAdsApiClient


api_client = GoogleAdsApiClient()


@admin.action(description="Request historical metrics")
def request_historical_metrics(modeladmin, request, queryset):
    regions_keyword = {}
    for obj in queryset.all():
        regions = tuple(obj.regions.values_list("id", flat=True))
        try:
            regions_keyword[regions].append(obj.text)
        except KeyError:
            regions_keyword[regions] = [obj.text]

    data = []
    import time

    for regions, keywords in regions_keyword.items():
        response = api_client.request_historical_keywords_metrics(keywords, regions)
        time.sleep(5)
        data.extend(response)

    today = datetime.now()
    metrics = []
    for row in data:
        keyword = queryset.filter(text__iexact=row["keyword"])
        for region_id in row["region_ids"]:
            keyword = keyword.filter(regions__id=region_id)

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
