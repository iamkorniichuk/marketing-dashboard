from datetime import datetime
import re

from ads.models import RegionAge, RegionGender, RegionViewers, TiktokAd
from campaigns.models import TiktokAdvertiser
from campaigns.spiders import crawl_websites
from regions.models import Region

from api_clients import TiktokLibraryApiClient, GoogleSearchApiClient


tiktok_library_api_client = TiktokLibraryApiClient()
search_api_client = GoogleSearchApiClient()


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
    # TODO: Add until_id
    advertisers = tiktok_library_api_client.request_ads(
        start_time=datetime(year=2024, month=1, day=1),
        end_time=datetime.now(),
    )

    objs = []
    adv_objs = []
    for adv_id, info in advertisers.items():
        adv_region = Region.objects.get(name=info["location"])
        adv_website = search_api_client.request_company_website(
            info["name"], adv_region.country_code
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
                    "first_shown": ad["first_shown"].date(),
                    "last_shown": ad["last_shown"].date(),
                    "total_viewers": number_repr_to_int(ad["audience"]),
                },
            )
            objs.append(obj)

            for data in ad["Age"]:
                region = Region.objects.get(name=data.pop("Country"))
                min_age, max_age = ages_to_range(data)
                RegionAge.objects.create(
                    ad=obj,
                    region=region,
                    min_age=min_age,
                    max_age=max_age,
                )

            for data in ad["Location"]:
                region = Region.objects.get(name=data["Country"])
                unique_viewers = number_repr_to_int(data["Unique users seen"])
                RegionViewers.objects.create(
                    ad=obj,
                    region=region,
                    unique_viewers=unique_viewers,
                )

            for data in ad["Gender"]:
                region = Region.objects.get(name=data["Country"])
                RegionGender.objects.create(
                    ad=obj,
                    region=region,
                    is_male=data["Male"],
                    is_female=data["Female"],
                    is_unknown=data["Unknown gender"],
                )

    crawl_websites(adv_objs)
    return objs
