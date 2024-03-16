import json
import requests
import pandas as pd


class CrossroadsApiClient:
    def __init__(self, crossroads_config: str):
        with open(crossroads_config) as file:
            self.credentials = json.load(file)
        self.base_url = "https://crossroads.domainactive.com/api/v2/"

    def build_url(self, endpoint):
        return self.base_url + endpoint

    def format_date(self, date):
        return date.strftime("%Y-%m-%d")

    def request_campaigns_report(self, start_date, end_date):
        full_url = self.build_url("get-campaigns-info")
        start_date = self.format_date(start_date)
        end_date = self.format_date(end_date)

        params = {
            "key": self.credentials["api_key"],
            "start-date": start_date,
            "end-date": end_date,
        }

        return requests.get(full_url, params=params).json()["campaigns_info"]

    def request_keywords_report(self, start_date, end_date):
        full_url = self.build_url("get-dynamic-landers")
        start_date = self.format_date(start_date)
        end_date = self.format_date(end_date)

        params = {
            "api_key": self.credentials["api_key"],
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.get(full_url, params=params)
        dataframe = pd.DataFrame(response.json())[
            [
                "campaign_id",
                "lander_keyword",
                "clicks",
            ]
        ]

        campaign_ids = []
        for campaign_id in dataframe["campaign_id"].unique().tolist():
            mask = dataframe["campaign_id"] == campaign_id
            top_keywords = (
                dataframe[mask].sort_values("clicks", ascending=False).head(3)
            )
            campaign_ids.append(top_keywords)

        completed_dataframe = pd.concat(campaign_ids)
        return completed_dataframe[completed_dataframe["campaign_id"].notnull()]
