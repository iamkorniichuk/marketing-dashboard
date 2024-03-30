import json
from paths import GOOGLE_SEARCH_CONFIG, OXYLABS_CONFIG


class GoogleSearchApiClient:
    def __init__(
        self,
        google_search_config: str = GOOGLE_SEARCH_CONFIG,
        oxylabs_config: str = OXYLABS_CONFIG,
    ):
        with open(google_search_config) as file:
            self.credentials = json.load(file)

        with open(oxylabs_config) as file:
            self.proxy_config = json.load(file)

        self.base_url = "https://cse.google.com/cse"

    def build_proxy(self, region_code):
        entry = f"http://customer-{self.proxy_config['username']}-cc-{region_code}:{self.proxy_config['password']}@pr.oxylabs.io:7777"
        return {
            "http": entry,
            "https": entry,
        }
