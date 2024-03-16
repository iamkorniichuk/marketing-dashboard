import json

from business_api_client.api import AuthenticationApi, ReportingApi
from business_api_client.api_client import ApiClient


class TiktokBusinessApiClient:
    def __init__(self, tiktok_business_config: str):
        with open(tiktok_business_config) as file:
            self.credentials = json.load(file)
        self.api_client = ApiClient()
        self.reporting_service = ReportingApi()
        self.authentication_service = AuthenticationApi(self.api_client)

    def format_date(self, date):
        return date.strftime("%Y-%m-%d")

    def request_advertisers(self):
        return self.authentication_service.oauth2_advertiser_get(
            app_id=self.credentials["app_id"],
            secret=self.credentials["secret"],
            access_token=self.credentials["access_token"],
        )["data"]["list"]

    def request_campaigns_report(self, advertiser_id, start_date, end_date):
        start_date = self.format_date(start_date)
        end_date = self.format_date(end_date)

        report_type = "BASIC"
        data_level = "AUCTION_CAMPAIGN"
        dimensions = ["campaign_id"]
        access_token = self.credentials["access_token"]
        data = [
            "campaign_name",
            "advertiser_id",
            "video_play_actions",
            "video_watched_2s",
            "video_watched_6s",
            "video_views_p25",
            "video_views_p50",
            "video_views_p75",
            "video_views_p100",
            "cost_per_conversion",
            "cpc",
            "ctr",
            "clicks",
            "spend",
            "conversion",
        ]

        response = self.reporting_service.report_integrated_get(
            advertiser_id,
            report_type=report_type,
            dimensions=dimensions,
            access_token=access_token,
            data_level=data_level,
            start_date=start_date,
            end_date=end_date,
            metrics=data,
        )

        results = []
        for row in response["data"]["list"]:
            data = row["metrics"]
            data["campaign_id"] = row["dimensions"]["campaign_id"]
            results.append(data)

        return results
