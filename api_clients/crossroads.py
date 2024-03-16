import json
import requests


class CrossroadsApiClient:
    def __init__(self, crossroads_config: str):
        self.credentials = json.loads(open(crossroads_config))
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
