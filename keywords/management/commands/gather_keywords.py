from datetime import datetime

from django.core.management.base import BaseCommand

from api_clients import TiktokBusinessApiClient, CrossroadsApiClient
from keywords.models import CrossroadsKeyword


class Command(BaseCommand):
    help = "Save keywords to a current database"

    def add_arguments(self, parser):
        parser.add_argument("crossroads", type=str)
        parser.add_argument("tiktok", type=str)

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.crossroads_api_client = CrossroadsApiClient(options["crossroads"])
        self.tiktok_business_api_client = TiktokBusinessApiClient(options["tiktok"])

        crossroads_keywords = self.gather_crossroads_keywords()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(crossroads_keywords)} Crossroads Keywords"
            )
        )

    def gather_crossroads_keywords(self):
        data = self.crossroads_api_client.request_keywords_report(
            self.datetime, self.datetime
        )

        keywords = []
        for row in data:
            keywords.append(
                CrossroadsKeyword(
                    campaign_id=row["campaign_id"],
                    lander_keyword=row["campaign_id"],
                    clicks=row["clicks"],
                    date=self.datetime.date(),
                )
            )

        return CrossroadsKeyword.objects.bulk_create(
            keywords,
            update_conflicts=True,
            unique_fields=["campaign_id", "lander_keyword", "date"],
            update_fields=["clicks"],
        )
