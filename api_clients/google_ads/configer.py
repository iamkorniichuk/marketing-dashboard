import json

from google.ads.googleads.client import GoogleAdsClient

from paths import GOOGLE_ADS_CONFIG, KEYWORD_REQUEST_CONFIG


class GoogleAdsConfiger:
    def __init__(
        self,
        google_ads_config: str = GOOGLE_ADS_CONFIG,
        request_config: str = KEYWORD_REQUEST_CONFIG,
    ):
        self.api_client = GoogleAdsClient.load_from_storage(google_ads_config)
        with open(request_config) as file:
            self.request_config = json.load(file)

        self.ads_service = self.api_client.get_service("GoogleAdsService")
        self.geo_service = self.api_client.get_service("GeoTargetConstantService")
        self.keyword_service = self.api_client.get_service("KeywordPlanIdeaService")
