import json
import requests
import pandas as pd
from urllib import parse

from business_api_client.api import AdApi, AuthenticationApi, ReportingApi
from business_api_client.api_client import ApiClient


class TiktokBusinessApiClient:
    def __init__(self, tiktok_business_config: str):
        with open(tiktok_business_config) as file:
            self.credentials = json.load(file)
        self.api_client = ApiClient()
        self.reporting_service = ReportingApi()
        self.authentication_service = AuthenticationApi(self.api_client)
        self.ad_service = AdApi(self.api_client)

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

    def request_crossroads_id(self, advertiser_id):
        response = self.ad_service.ad_get(
            advertiser_id,
            self.credentials["access_token"],
        )
        dataframe = pd.DataFrame(response["data"]["list"])
        dataframe.drop_duplicates("campaign_id", keep="last", inplace=True)
        dataframe["cr_campaign_id"] = dataframe.apply(
            lambda row: self.extract_crossroads_id(row["landing_page_url"]),
            axis=1,
        )
        dataframe = dataframe[dataframe["cr_campaign_id"].notnull()]
        return dataframe[["cr_campaign_id", "campaign_id"]].to_dict("records")

    def extract_crossroads_id(self, url):
        try:
            initial_url = parse.urlparse(url)
            is_valid = all([initial_url.scheme, initial_url.netloc])

            if is_valid:
                response = requests.get(url)
                redirect_url = parse.urlparse(response.url)
                url_params = parse.parse_qs(redirect_url.query)
                cr_campaign_id = url_params["acid"]
                return cr_campaign_id[0]
        except Exception:
            pass
