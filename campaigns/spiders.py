import re
from urllib.parse import urlparse
from threading import Thread

from django.conf import settings

from scrapy import Item, Field
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule

from campaigns.models import TiktokAdvertiser


class TiktokAdvertiserSavePipeline:
    def process_item(self, item, spider):
        print(item)
        obj, _ = TiktokAdvertiser.objects.update_or_create(
            id=item["model_id"],
            defaults={
                "website": item.get("website", None),
                "phone_number": item.get("phone_number", ""),
                "email": item.get("email", None),
                "youtube": item.get("youtube", None),
                "linkedin": item.get("linkedin", None),
                "facebook": item.get("facebook", None),
            },
        )
        return item


class TiktokAdvertiserItem(Item):
    model_id = Field()
    website = Field()
    email = Field()
    phone_number = Field()
    facebook = Field()
    linkedin = Field()
    youtube = Field()


class ContactsSpider(CrawlSpider):
    name = "contacts_extractor"
    custom_settings = {
        "ITEM_PIPELINES": {
            "campaigns.spiders.TiktokAdvertiserSavePipeline": 300,
        }
    }
    sticky_meta_keys = ["model_id", "website"]

    def __init__(self, items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items
        domains = [urlparse(obj["website"]).netloc for obj in items]
        self.rules = [
            Rule(
                LinkExtractor(allow_domains=domains, unique=True),
                callback=self.parse_contacts,
                follow=True,
            )
        ]
        self._compile_rules()

    def start_requests(self):
        for obj in self.items:
            yield Request(
                url=obj["website"],
                meta={"model_id": obj["model_id"], "website": obj["website"]},
                callback=self.parse_contacts,
                dont_filter=True,
            )

    def parse_contacts(self, response):
        def is_response_text(response):
            try:
                response.text
                return True
            except AttributeError:
                return False

        patterns = {
            "email": r"([A-Za-z0-9]+[._])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            "phone_number": r"\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})",
            "facebook": r"https?://(www\.)?(mbasic\.facebook|m\.facebook|facebook|fb)\.(com|me)\/(?:[^\s\/?]+)?(?:\?|\/|$)",
            "linkedin": r"https?://(www\.)?linkedin\.com/company/[\w-]+(?=[^\w-]|$)",
            "youtube": r"https?://(www\.)?(youtube\.com\/channel\/)(?:[^\s\/?]+)?(?:\?|\/|$)",
        }

        if is_response_text(response):
            data = {}
            for name, pattern in patterns.items():
                matches = re.search(pattern, response.text, re.IGNORECASE)
                if matches:
                    data[name] = matches.group()

            yield TiktokAdvertiserItem(
                model_id=response.meta["model_id"],
                website=response.meta["website"],
                **data,
            )


def crawl_websites(models):
    def run():
        process = CrawlerProcess(settings.SCRAPY)
        process.crawl(
            ContactsSpider,
            items=[{"model_id": obj.id, "website": obj.website} for obj in models],
        )
        process.start(stop_after_crawl=True, install_signal_handlers=False)

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
