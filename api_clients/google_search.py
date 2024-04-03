import json
from requests import PreparedRequest
from urllib.parse import urlencode
from bs4 import BeautifulSoup, ResultSet

from seleniumwire.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from paths import GOOGLE_SEARCH_CONFIG, OXYLABS_CONFIG
from commons.design_patterns import Singleton


def safe_selenium_request(default=None):
    def decorator(request_function):
        def wrapper(*args, **kwargs):
            try:
                return request_function(*args, **kwargs)
            except TimeoutException:
                return default

        return wrapper

    return decorator


class GoogleSearchApiClient(metaclass=Singleton):
    def __init__(
        self,
        google_search_config: str = GOOGLE_SEARCH_CONFIG,
        oxylabs_config: str = OXYLABS_CONFIG,
    ):
        with open(google_search_config) as file:
            self.credentials = json.load(file)

        with open(oxylabs_config) as file:
            self.proxy_config = json.load(file)
        # TODO: Does it always 26%?
        self.base_url = "https://cse.google.com/cse"

    def request_keywords_competition(self, keywords, region_code):
        results = {}

        for word in keywords:
            results[word] = self.request_one_keyword_competition(word, region_code)

        return results

    def request_one_keyword_competition(self, keyword, region_code, pages=2):
        free_pages = ResultSet([])
        sponsored_pages = ResultSet([])
        for i in range(pages):
            response = self.request_query_search(keyword, region_code, page=i)
            soup = BeautifulSoup(response, "html.parser")

            sponsored_pages.extend(
                soup.select("div.i_.clicktrackedAd_js.styleable-rootcontainer")
            )
            free_pages.extend(soup.select("div.gsc-webResult.gsc-result"))

        total_pages_number = len(free_pages) + len(sponsored_pages)
        result = len(sponsored_pages) / total_pages_number * 100

        return int(result)

    def build_webdriver(
        self,
        options_arguments=[],
        seleniumwire_options={},
    ) -> Firefox:
        driver_options = FirefoxOptions()
        for argument in options_arguments:
            driver_options.add_argument(argument)

        return Firefox(
            options=driver_options,
            seleniumwire_options=seleniumwire_options,
        )

    def request_query_search(self, query, region_code, page=0) -> str:
        @safe_selenium_request(default="")
        def extract_ad_iframe(webdriver):
            wait = WebDriverWait(webdriver, 10)
            iframe = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#master-1"))
            )
            webdriver.switch_to.frame(iframe)
            source = webdriver.page_source
            webdriver.switch_to.default_content()
            return source

        proxy = self.build_proxy(region_code)
        webdriver = self.build_webdriver(
            options_arguments=["--headless"],
            seleniumwire_options={"proxy": proxy},
        )
        url = self.build_url(query, page)
        webdriver.get(url)

        ads_page = extract_ad_iframe(webdriver)
        whole_page = webdriver.page_source

        return whole_page + ads_page

    def build_url(self, search, page=0):
        request = PreparedRequest()
        params = {
            "cx": self.credentials["search_engine_id"],
            "key": self.credentials["api_key"],
            "q": search,
        }
        request.prepare_url(self.base_url, params)
        fragments = urlencode(
            {
                "gsc.tab": 0,
                "gsc.q": search,
                "gsc.page": page + 1,
            }
        )
        return f"{request.url}#{fragments}"

    def build_proxy(self, region_code):
        entry = f"http://customer-{self.proxy_config['username']}-cc-{region_code}:{self.proxy_config['password']}@pr.oxylabs.io:7777"
        return {
            "http": entry,
            "https": entry,
        }
