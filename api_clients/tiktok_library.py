from datetime import datetime
import json
from urllib.parse import urlencode, parse_qs, urlparse
import pandas as pd
import re

from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from paths import OXYLABS_CONFIG
from commons.design_patterns import Singleton


def find_recursive_parent(element, name, attrs):
    cursor = element.parent
    is_match = lambda el: el.name == name and all(
        [el[key] == value for key, value in attrs.items() if el.has_attr(key)]
    )
    while cursor is not None:
        if is_match(cursor):
            return cursor
        element = cursor.find_previous(name, attrs, recursive=False)
        if element:
            return element
        cursor = cursor.parent


class TiktokLibraryApiClient(metaclass=Singleton):
    def __init__(self):
        with open(OXYLABS_CONFIG) as file:
            self.proxy_config = json.load(file)
        self.base_url = "https://library.tiktok.com"

    def request_ad_hrefs(
        self, webdriver, start_time, end_time, repeat=5, until_id=None
    ):
        params = urlencode(
            {
                "region": "all",
                "start_time": int(start_time.timestamp()) * 1000,
                "end_time": int(end_time.timestamp()) * 1000,
                "sort_type": "last_shown_date,desc",
            }
        )
        url = f"{self.base_url}/ads?{params}"

        webdriver.get(url)

        if until_id:
            import time

            print(until_id)
            time.sleep(10)
            while not EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'a.link[href*="{until_id}"]')
            ):
                self.load_more(webdriver)
        else:
            for _ in range(repeat):
                self.load_more(webdriver)

        cards_soup = BeautifulSoup(webdriver.page_source, "html.parser")

        ads = cards_soup.select("div.ad_card")
        hrefs = []
        for div in ads:
            url = f'{self.base_url}{div.select_one("a.link")["href"]}'
            if until_id and f"ad_id={until_id}" in url:
                break
            hrefs.append(url)

        return hrefs

    def request_ad_details(self, webdriver, hrefs):
        advertisers = {}
        for url in hrefs:
            data = {"link": url}

            webdriver.get(data["link"])
            wait = WebDriverWait(webdriver, 20)
            try:
                advertiser_a_tag = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'a.item_link[href*="adv_biz_ids"]')
                    )
                )
            except TimeoutException:
                continue
            ad_soup = BeautifulSoup(webdriver.page_source, "html.parser")

            data.update(
                self.parse_ad_details(ad_soup.select_one("div.ad_detail_video_card"))
            )
            data.update(self.parse_ad_page(ad_soup))
            try:
                advertisers[data["advertiser_id"]]["ads"].append(data)
            except KeyError:
                webdriver.get(advertiser_a_tag.get_attribute("href"))
                wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.ad_card"))
                )
                adv_soup = BeautifulSoup(webdriver.page_source, "html.parser")
                total_ads_text = adv_soup.select_one("div.total_ads").get_text()

                advertisers[data["advertiser_id"]] = {
                    "ads": [data],
                    "name": data["Advertiser"],
                    "location": data["Advertiser's registered location"],
                    "url": data["advertiser_url"],
                    "total_ads": self.parse_total_ads(total_ads_text),
                }
        return advertisers

    def parse_total_ads(self, text):
        pattern = r"(?:\d+,)*\d+"

        match = re.search(pattern, text)
        if match:
            number = int(match.group().replace(",", ""))
            return number

    def parse_ad_details(self, div):
        headers = [div.get_text() for div in div.select("div.ad_advertiser")]
        data = {}
        for i, tag in enumerate(div.select("div.ad_advertiser_value")):
            data[headers[i]] = tag.get_text()

        data["advertiser_url"] = (
            f'{self.base_url}/{div.select_one("a.item_link")["href"]}'
        )
        url = urlparse(data["advertiser_url"])
        data["advertiser_id"] = parse_qs(url.query)["adv_biz_ids"][0]

        return data

    def parse_ad_table(self, table):
        thead_tr = table.find("thead").find("tr")
        headers = [th.get_text() for th in thead_tr.select("th")]

        rows = []
        tbody_tr = table.find("tbody").select("tr")
        for tr in tbody_tr:
            data = {}
            for i, td in enumerate(tr.select("td")):
                svg = td.select_one("svg")
                if svg:
                    value = svg["color"] == "#FE2C55"
                else:
                    value = td.get_text()

                data[headers[i]] = value
            rows.append(data)
        df = pd.DataFrame(rows)
        if "Number" in df.columns:
            df.set_index("Number", inplace=True)
        return df.to_dict("records")

    def parse_ad_summary(self, container):
        pattern = r"^[A-Za-z0-9 ]*"

        headers = []
        for span in container.select("span.item_title"):
            matches = re.search(pattern, span.get_text())
            headers.append(matches.group())

        data = {}
        for i, tag in enumerate(container.select("span.item_value")):
            data[headers[i]] = tag.get_text()

        return data

    def parse_ad_page(self, page):
        data = {}
        for tag in page.select("table.byted-Table-Implement"):
            h2 = find_recursive_parent(
                tag, "h2", {"class": "ad_details_targeting_title"}
            )
            data[h2.get_text()] = self.parse_ad_table(tag)

        span = page.select_one("span.ad_unique_identifier_text")
        data["id"] = re.search(r"\d+", span.get_text()).group()
        data["audience"] = page.select_one(
            "span.ad_target_audience_size_value"
        ).get_text()

        summary = self.parse_ad_summary(
            page.select_one("ul.ad_detail_module_container")
        )
        data.update(summary)

        return data

    def str_to_datetime(self, value):
        return datetime.strptime(value, "%m/%d/%Y")

    def load_more(self, webdriver):
        wait = WebDriverWait(webdriver, 10)
        load_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.loading_more_text"))
        )
        load_button.click()
