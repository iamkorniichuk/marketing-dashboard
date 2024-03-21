import json
from typing import Iterable

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

    def format_cost(self, number: str) -> str:
        divided_number = int(number) / 1000000
        rounded_result = round(divided_number, 1)
        return f"${rounded_result}"

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
