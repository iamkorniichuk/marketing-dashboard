from datetime import datetime, timedelta
from typing import Iterable
from django.db.models import QuerySet

from api_clients import ChatGptApiClient, GoogleAdsApiClient

from keywords.models import BaseKeyword, ChatGptKeyword
from regions.models import Region


chat_gpt_api_client = ChatGptApiClient()
google_ads_api_client = GoogleAdsApiClient()


def generate_similar_keywords(
    queryset: QuerySet[BaseKeyword], regions: Iterable[Region], cpc_limit: float
) -> Iterable[ChatGptKeyword]:
    keywords = queryset.values_list("text", flat=True)
    region_ids = [obj.id for obj in regions]
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(weeks=2)

    suggestions = chat_gpt_api_client.request_keyword_suggestions(keywords)
    data = google_ads_api_client.request_forecast_keywords_metrics(
        suggestions, region_ids, start_date, end_date
    )

    for row in data:
        if row["avg_cpc"] >= cpc_limit:
            obj, _ = ChatGptKeyword.objects.get_or_create(text=row["keyword"])
            obj.based_on.set(queryset)


def generate_marketing_type_choice(queryset: QuerySet[BaseKeyword]):
    keywords = queryset.values_list("text", flat=True)
    choices = chat_gpt_api_client.request_marketing_type_choice(keywords)

    objs = []
    for text, marketing in choices.items():
        obj = queryset.filter(text__iexact=text).first()
        if obj:
            obj.marketing = marketing
            objs.append(obj)

    BaseKeyword.objects.bulk_update(objs, ["marketing"])
