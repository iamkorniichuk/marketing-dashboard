import json
from typing import Iterable
from datetime import datetime
import pandas as pd

from google.ads.googleads.client import GoogleAdsClient


class GoogleAdsApiClient:
    def __init__(self, google_ads_config: str, request_config: str):
        self.api_client = GoogleAdsClient.load_from_storage(google_ads_config)
        with open(request_config) as file:
            self.request_config = json.load(file)

        self.ads_service = self.api_client.get_service("GoogleAdsService")
        self.geo_service = self.api_client.get_service("GeoTargetConstantService")
        self.keyword_service = self.api_client.get_service("KeywordPlanIdeaService")

    def format_date(self, date):
        return date.strftime("%Y-%m-%d")

    def format_micros(self, number: str) -> float:
        divided_number = int(number) / 1_000_000
        return round(divided_number, 2)

    def build_regions(self, region_ids: Iterable[str]):
        results = []
        for region in region_ids:
            results.append(self.geo_service.geo_target_constant_path(region))

        return results

    def build_language(self, language_id: str):
        return self.ads_service.language_constant_path(language_id)

    def get_keyword_level(self, is_partners_included: bool):
        if is_partners_included:
            result = (
                self.api_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
            )
        else:
            result = self.api_client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        return result

    def request_historical_keywords_metrics(
        self, keywords: Iterable[str], region_ids: Iterable[str]
    ):
        solo_response = self._request_historical_keywords_metrics(
            keywords,
            region_ids,
            is_partners_included=False,
        )
        partners_response = self._request_historical_keywords_metrics(
            keywords,
            region_ids,
            is_partners_included=True,
        )
        solo_dataframe = pd.DataFrame(solo_response)
        partners_dataframe = pd.DataFrame(partners_response)

        dataframe = solo_dataframe.merge(
            partners_dataframe, on="keyword", suffixes=("", "_partners")
        )

        dataframe["date"] = self.format_date(datetime.now().date())
        dataframe["region_ids"] = [region_ids for i in dataframe.index]
        return dataframe.to_dict("records")

    def _request_historical_keywords_metrics(
        self,
        keywords: Iterable[str],
        region_ids: Iterable[str],
        is_partners_included: bool,
    ):
        request = self.api_client.get_type("GenerateKeywordHistoricalMetricsRequest")
        request.historical_metrics_options.include_average_cpc = True
        request.customer_id = self.request_config["customer_id"]
        request.language = self.build_language(self.request_config["language_id"])
        request.geo_target_constants.extend(self.build_regions(region_ids))
        request.include_adult_keywords = self.request_config["include_adult_keywords"]
        request.keyword_plan_network = self.get_keyword_level(is_partners_included)
        request.keywords.extend(keywords)

        response = self.keyword_service.generate_keyword_historical_metrics(
            request=request
        )

        data = [
            {
                "keyword": element.text,
                "avg_month_search": element.keyword_metrics.avg_monthly_searches,
                "avg_cpc": self.format_micros(
                    element.keyword_metrics.average_cpc_micros
                ),
                "low_page_bid": self.format_micros(
                    element.keyword_metrics.low_top_of_page_bid_micros
                ),
                "high_page_bid": self.format_micros(
                    element.keyword_metrics.high_top_of_page_bid_micros
                ),
            }
            for element in response.results
        ]
        return data
