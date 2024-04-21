import re
from threading import Thread

from django.conf import settings

from scrapy import Item, Field
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy import signals
from pydispatch import dispatcher
from crochet import setup

from campaigns.models import TiktokAdvertiser


class TiktokAdvertiserSavePipeline:
    def process_item(self, item, spider):
        fields = [
            "website",
            "phone_number",
            "email",
            "youtube",
            "linkedin",
            "facebook",
        ]
        defaults = {}
        for name in fields:
            if name in item:
                defaults[name] = item[name]

        obj, _ = TiktokAdvertiser.objects.update_or_create(
            id=item["model_id"],
            defaults=defaults,
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
        },
        "DEPTH_LIMIT": 1,
    }
    sticky_meta_keys = ["model_id", "website"]

    def __init__(self, items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dispatcher.connect(self.closed, signals.spider_closed)
        self.items = items
        self.rules = [
            Rule(
                LinkExtractor(unique=True),
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
            )

    def parse_contacts(self, response):
        def is_response_text(response):
            try:
                response.text
                return True
            except AttributeError:
                return False

        if "policies/contact-information" in response.url:
            import os

            print("WIN!")
            os._exit(1)

        for url in response.css("a::attr(href)").getall():
            yield response.follow(url, self.parse_contacts)

        patterns = {
            "email": r"[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}(\.[a-zA-Z]{2,6})?",
            "phone_number": r"(1[ \-\+]{0,3}|\+1[ -\+]{0,3}|\+1|\+)?((\(\+?1-[2-9][0-9]{1,2}\))|(\(\+?[2-8][0-9][0-9]\))|(\(\+?[1-9][0-9]\))|(\(\+?[17]\))|(\([2-9][2-9]\))|([ \-\.]{0,3}[0-9]{2,4}))?([ \-\.][0-9])?([ \-\.]{0,3}[0-9]{2,4}){2,3}",
            "facebook": r"(https://)?(www\.)?(mbasic\.facebook|m\.facebook|facebook|fb)\.(com|me)\/(?:[^\s\/?]+)?(?:\?|\/|$)",
            "linkedin": r"(https://)?(www\.)?linkedin\.com/company/[\w-]+(?=[^\w-]|$)",
            "youtube": r"(https://)?(www\.)?(youtube\.com\/channel\/)(?:[^\s\/?]+)?(?:\?|\/|$)",
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

    def closed(self, reason):
        crawled_urls = self.crawler.stats.get_value("response_received_count")
        print(f"Total crawled URLs: {crawled_urls}")
        item_count = self.crawler.stats.get_value("item_scraped_count")
        print(f"Total contacts found: {item_count}")
        elapsed_time = self.crawler.stats.get_value("elapsed_time_seconds")
        print(f"Elapsed time: {elapsed_time}")


def crawl_websites(models):
    def run():
        setup()
        process = CrawlerProcess(settings.SCRAPY)
        process.crawl(
            ContactsSpider,
            items=[{"model_id": obj.id, "website": obj.website} for obj in models],
        )
        process.start(stop_after_crawl=False, install_signal_handlers=False)

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
