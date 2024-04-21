import json
from requests import PreparedRequest
from urllib.parse import urlencode

import requests
from commons.webdriver import DisplayWebdriver
from bs4 import BeautifulSoup, ResultSet

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
            except:
                return default

        return wrapper

    return decorator


class GoogleSearchApiClient(metaclass=Singleton):
    def __init__(self):
        with open(GOOGLE_SEARCH_CONFIG) as file:
            self.credentials = json.load(file)

        with open(OXYLABS_CONFIG) as file:
            self.proxy_config = json.load(file)
        self.base_url = "https://cse.google.com/cse"

    @safe_selenium_request(default="")
    def request_company_website(self, webdriver, name):
        response = self.request_query_search(webdriver, name, page=0, with_ads=False)
        soup = BeautifulSoup(response, "html.parser")
        for result in soup.select("div.gsc-webResult.gsc-result"):
            a = result.select_one("a.gs-title")
            if a:
                url = a["href"]
                response = requests.get(url, allow_redirects=False)
                if response.status_code < 400:
                    return url

    def request_keywords_competition(self, keywords, region_code):
        results = {}

        for word in keywords:
            results[word] = self.request_one_keyword_competition(word, region_code)

        return results

    def request_one_keyword_competition(self, keyword, region_code, pages=2):
        free_pages = ResultSet([])
        sponsored_pages = ResultSet([])
        proxy = self.build_proxy(region_code)
        with DisplayWebdriver(proxy=proxy) as webdriver:
            for i in range(pages):
                response = self.request_query_search(
                    webdriver, keyword, page=i, with_ads=True
                )
                soup = BeautifulSoup(response, "html.parser")

                sponsored_pages.extend(
                    soup.select("div.i_.clicktrackedAd_js.styleable-rootcontainer")
                )
                free_pages.extend(soup.select("div.gsc-webResult.gsc-result"))

        return len(sponsored_pages), len(free_pages)

    def request_query_search(self, webdriver, query, page=0, with_ads=True):
        url = self.build_url(query, page)
        webdriver.get(url)

        wait = WebDriverWait(webdriver, 40)
        if with_ads:
            iframe = safe_selenium_request(default="")(wait.until)(
                (EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#master-1")))
            )

            whole_page = webdriver.page_source
            webdriver.switch_to.frame(iframe)
            ads_page = webdriver.page_source

            return whole_page + ads_page
        else:
            safe_selenium_request()(wait.until)(
                (
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.gsc-webResult.gsc-result")
                    )
                )
            )
            return webdriver.page_source

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
