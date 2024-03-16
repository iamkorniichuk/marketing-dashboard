import json

from business_api_client.api import AuthenticationApi
from business_api_client.api_client import ApiClient


class TikTokBusinessApiClient:
    def __init__(self, tiktok_business_config: str):
        self.credentials = json.loads(open(tiktok_business_config))
        self.api_client = ApiClient()

    def get_advertisers(self):
        authentication_service = AuthenticationApi(self.api_client)
        return authentication_service.oauth2_advertiser_get(
            app_id=self.credentials["app_id"],
            secret=self.credentials["secret"],
            access_token=self.credentials["access_token"],
        )["data"]["list"]
