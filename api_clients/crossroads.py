import json


class CrossroadsApiClient:
    def __init__(self, crossroads_config: str):
        self.credentials = json.loads(open(crossroads_config))
        self.base_url = "https://crossroads.domainactive.com/api/v2/"

    def build_url(self, endpoint):
        return self.base_url + endpoint
