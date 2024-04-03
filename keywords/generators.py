from typing import Iterable
from django.db.models import QuerySet

from api_clients import ChatGptApiClient, GoogleAdsApiClient

from keywords.models import Keyword
from regions.models import Region


chat_gpt_api_client = ChatGptApiClient()
google_ads_api_client = GoogleAdsApiClient()


def generate_similar_keywords(
    queryset: QuerySet[Keyword], regions: Iterable[Region]
) -> Iterable[Keyword]:
    keywords = queryset.values_list("text", flat=True)
    suggestions = chat_gpt_api_client.request_keyword_suggestions(keywords)
    results = []
    for text in suggestions:
        obj, _ = Keyword.objects.get_or_create(
            text=text,
            defaults={"is_generated_by_chat_gpt": True},
        )
        results.append(obj)
    return results
