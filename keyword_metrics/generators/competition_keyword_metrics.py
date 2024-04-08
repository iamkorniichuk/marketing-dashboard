from datetime import datetime
from django.db.models import QuerySet
from django.core.files.base import ContentFile
import pandas as pd
from io import BytesIO

from keywords.models import BaseKeyword
from regions.models import Region
from keyword_metrics.models import GoogleSearchKeywordMetrics

from api_clients import GoogleSearchApiClient, GoogleAdsApiClient


search_api_client = GoogleSearchApiClient()
ads_api_client = GoogleAdsApiClient()


def generate_keyword_competition(queryset: QuerySet[BaseKeyword], region: Region):
    keywords = queryset.values_list("text", flat=True)
    data = ads_api_client.request_historical_keywords_metrics(keywords, [region.id])

    date = datetime.now().date()
    results = []
    for row in data:
        keyword = row["keyword"]
        sponsored_results, common_results = (
            search_api_client.request_one_keyword_competition(
                keyword, region.country_code
            )
        )
        exact_keywords = queryset.filter(text__iexact=keyword)
        obj, _ = GoogleSearchKeywordMetrics.objects.update_or_create(
            keyword=exact_keywords.first(),
            date=date,
            region=region,
            defaults={
                "sponsored_results": sponsored_results,
                "common_results": common_results,
                "average_cpc": row["avg_cpc"],
                "partners_average_cpc": row["avg_cpc_partners"],
                "low_page_bid": row["low_page_bid"],
                "partners_low_page_bid": row["low_page_bid_partners"],
                "high_page_bid": row["high_page_bid"],
                "partners_high_page_bid": row["high_page_bid_partners"],
            },
        )
        import matplotlib

        matplotlib.use("agg")
        volume_dataframe = pd.DataFrame.from_dict(row["monthly_volumes"])
        volume_plot = volume_dataframe.plot.bar(
            use_index=True, y="monthly_searches", width=0.9, figsize=(6, 3)
        )

        volume_plot.set_title(None)
        volume_plot.set_xlabel(None)
        volume_plot.set_ylabel(None)
        volume_plot.legend().remove()
        volume_plot.spines["top"].set_visible(False)
        volume_plot.spines["right"].set_visible(False)
        volume_plot.spines["left"].set_visible(False)
        volume_plot.spines["bottom"].set_visible(False)
        volume_plot.tick_params(axis="both", which="both", length=0)
        volume_plot.set_xticklabels([])
        volume_plot.set_yticklabels([])
        volume_plot.grid(False)

        bytes = BytesIO()
        volume_plot.get_figure().savefig(bytes, format="png")
        obj.volume_trends_image.save(f"{obj.id}.png", ContentFile(bytes.getvalue()))

        results.append(obj)

    return results
