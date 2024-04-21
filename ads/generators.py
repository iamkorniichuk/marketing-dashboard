from datetime import datetime
import re
import random

from ads.models import RegionAge, RegionGender, RegionViewers, TiktokAd
from campaigns.models import TiktokAdvertiser
from campaigns.spiders import crawl_websites
from commons.webdriver import DisplayWebdriver
from regions.models import Region

from api_clients import TiktokLibraryApiClient, GoogleSearchApiClient


tiktok_library_api_client = TiktokLibraryApiClient()
search_api_client = GoogleSearchApiClient()


def set_user_agent(webdriver, platform, user_agent):
    webdriver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {"userAgent": user_agent, "platform": platform},
    )


def number_repr_to_int(repr):
    suffix_multiplier = {"K": 1000, "M": 1000000, "B": 1000000000}

    pattern = r"(\d+\.?\d*)([KkMmBb]?)"
    match = re.match(pattern, repr)

    if match:
        number = float(match.group(1))
        suffix = match.group(2).upper()

        if suffix in suffix_multiplier:
            number *= suffix_multiplier[suffix]

        return int(number)
    else:
        return None


def ages_to_range(ages):
    results = []
    for age_range, is_included in ages.items():
        if is_included:
            numbers = map(int, re.findall(r"(\d.)", age_range))
            results.extend(numbers)

    return min(results), max(results)


def generate_ads():
    last = TiktokAd.objects.order_by("-id").first()
    until_id = None
    if last:
        until_id = last.id

    objs = []
    adv_objs = []
    with DisplayWebdriver() as webdriver:
        request_hrefs_kwargs = {
            "webdriver": webdriver,
            "start_time": datetime(year=2024, month=1, day=1),
            "end_time": datetime.now(),
        }
        if until_id:
            request_hrefs_kwargs["until_id"] = until_id
        else:
            request_hrefs_kwargs["repeat"] = 50

        urls = tiktok_library_api_client.request_ad_hrefs(**request_hrefs_kwargs)

        advertisers = tiktok_library_api_client.request_ad_details(webdriver, urls)

        user_agents = [
            {
                "device": "windows",
                "useragent": "Mozilla/5.0 (Windows NT 10.2; x64; en-US) Gecko/20130401 Firefox/64.6",
            },
            {
                "device": "windows",
                "useragent": "Mozilla/5.0 (Windows; U; Windows NT 10.3; x64) AppleWebKit/537.40 (KHTML, like Gecko) Chrome/47.0.3786.374 Safari/602.5 Edge/18.40967",
            },
            {
                "device": "mobile",
                "useragent": "Mozilla/5.0 (iPad; CPU iPad OS 8_0_8 like Mac OS X) AppleWebKit/533.19 (KHTML, like Gecko) Chrome/54.0.3831.205 Mobile Safari/534.0",
            },
            {
                "device": "mac",
                "useragent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_9) Gecko/20130401 Firefox/56.1",
            },
            {
                "device": "explorer",
                "useragent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; en-US Trident/5.0)",
            },
            {
                "device": "edge",
                "useragent": "Mozilla/5.0 (Windows; U; Windows NT 10.0;) AppleWebKit/602.22 (KHTML, like Gecko) Chrome/49.0.1224.183 Safari/602.0 Edge/18.87882",
            },
            {
                "device": "chrome",
                "useragent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; en-US) AppleWebKit/602.40 (KHTML, like Gecko) Chrome/47.0.1047.276 Safari/602",
            },
            {
                "device": "iphone",
                "useragent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_9; like Mac OS X) AppleWebKit/533.17 (KHTML, like Gecko) Chrome/53.0.1219.244 Mobile Safari/533.3",
            },
            {
                "device": "linux",
                "useragent": "Mozilla/5.0 (Linux i656 x86_64; en-US) Gecko/20100101 Firefox/63.2",
            },
            {
                "device": "edge",
                "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; en-US) AppleWebKit/602.27 (KHTML, like Gecko) Chrome/55.0.1651.233 Safari/602.0 Edge/9.40735",
            },
        ]

        default_region = Region.objects.filter(country_code="GB").first()
        for adv_id, info in advertisers.items():
            agent = random.choice(user_agents)
            set_user_agent(webdriver, agent["device"], agent["useragent"])
            adv_region = Region.objects.filter(name=info["location"]).first()
            if adv_region is None:
                adv_region = default_region

            webdriver.proxy = search_api_client.build_proxy(adv_region.country_code)
            adv_website = search_api_client.request_company_website(
                webdriver, info["name"]
            )
            adv, _ = TiktokAdvertiser.objects.get_or_create(
                id=adv_id,
                defaults={
                    "name": info["name"],
                    "region": adv_region,
                    "total_ads": info["total_ads"],
                    "website": adv_website,
                },
            )
            adv_objs.append(adv)
            for ad in info["ads"]:
                obj, _ = TiktokAd.objects.get_or_create(
                    id=ad["id"],
                    defaults={
                        "advertiser": adv,
                        "paid_for": ad["Ad paid for by"],
                        "first_shown": tiktok_library_api_client.str_to_datetime(
                            ad["First shown"]
                        ).date(),
                        "last_shown": tiktok_library_api_client.str_to_datetime(
                            ad["Last shown"]
                        ).date(),
                        "unique_viewers": number_repr_to_int(ad["Unique users seen"]),
                        "total_viewers": number_repr_to_int(ad["audience"]),
                    },
                )
                objs.append(obj)

                for data in ad["Age"]:
                    region = Region.objects.filter(name=data["Country"]).first()
                    if region is None:
                        region = default_region
                    min_age, max_age = ages_to_range(data)
                    RegionAge.objects.create(
                        ad=obj,
                        region=region,
                        min_age=min_age,
                        max_age=max_age,
                    )

                for data in ad["Location"]:
                    region = Region.objects.filter(name=data["Country"]).first()
                    if region is None:
                        region = default_region
                    unique_viewers = number_repr_to_int(data["Unique users seen"])
                    RegionViewers.objects.create(
                        ad=obj,
                        region=region,
                        unique_viewers=unique_viewers,
                    )

                for data in ad["Gender"]:
                    region = Region.objects.filter(name=data["Country"]).first()
                    if region is None:
                        region = default_region
                    RegionGender.objects.create(
                        ad=obj,
                        region=region,
                        is_male=data["Male"],
                        is_female=data["Female"],
                        is_unknown=data["Unknown gender"],
                    )

    crawl_websites(adv_objs)
    return objs
