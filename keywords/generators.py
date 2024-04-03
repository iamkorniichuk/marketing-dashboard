from datetime import datetime, timedelta
from typing import Iterable
from django.db.models import QuerySet

from api_clients import ChatGptApiClient, GoogleAdsApiClient

from keywords.models import Keyword
from regions.models import Region


chat_gpt_api_client = ChatGptApiClient()
google_ads_api_client = GoogleAdsApiClient()


def generate_similar_keywords(
    queryset: QuerySet[Keyword], regions: Iterable[Region], cpc_limit: float
) -> Iterable[Keyword]:
    keywords = queryset.values_list("text", flat=True)
    region_ids = [obj.id for obj in regions]
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(weeks=2)

    suggestions = chat_gpt_api_client.request_keyword_suggestions(keywords)
    data = google_ads_api_client.request_forecast_keywords_metrics(
        suggestions, region_ids, start_date, end_date
    )

    objs = []
    for row in data:
        if row["avg_cpc"] > cpc_limit:
            objs.append(
                Keyword(
                    text=row["keyword"],
                    is_generated_by_chat_gpt=True,
                )
            )

    Keyword.objects.bulk_create(
        objs,
        update_conflicts=True,
        update_fields=["is_generated_by_chat_gpt"],
        unique_fields=["text"],
    )
    return objs
