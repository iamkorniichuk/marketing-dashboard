from datetime import datetime
from paths import CROSSROADS_CONFIG

from django.core.management.base import BaseCommand

from api_clients import CrossroadsApiClient
from campaigns.models import CrossroadsCampaign

from metrics.models import CrossroadsKeywordMetrics


class Command(BaseCommand):
    help = "Load crossroads keyword metrics to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "-cfg",
            "--config",
            dest="config",
            type=str,
            default=CROSSROADS_CONFIG,
        )

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.api_client = CrossroadsApiClient(options["config"])

        data = self.api_client.request_keywords_report(self.datetime, self.datetime)
        keywords = []
        for row in data:
            campaign = CrossroadsCampaign.objects.filter(id=row["campaign_id"]).first()
            if campaign:
                keywords.append(
                    CrossroadsKeywordMetrics(
                        campaign=campaign,
                        lander_keyword=row["lander_keyword"],
                        clicks=row["clicks"],
                        date=self.datetime.date(),
                    )
                )

        results = CrossroadsKeywordMetrics.objects.bulk_create(
            keywords,
            update_conflicts=True,
            unique_fields=["campaign", "lander_keyword", "date"],
            update_fields=["clicks"],
        )
