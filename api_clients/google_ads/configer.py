import json

from paths import KEYWORD_REQUEST_CONFIG

from .utils import initialize_google_ads_client


class GoogleAdsConfiger:
    def __init__(self):
        self.api_client = initialize_google_ads_client()
        with open(KEYWORD_REQUEST_CONFIG) as file:
            self.request_config = json.load(file)

        self.ads_service = self.api_client.get_service("GoogleAdsService")
        self.geo_service = self.api_client.get_service("GeoTargetConstantService")
        self.keyword_service = self.api_client.get_service("KeywordPlanIdeaService")
