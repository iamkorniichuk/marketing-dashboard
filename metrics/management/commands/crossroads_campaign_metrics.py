from datetime import datetime

from django.core.management.base import BaseCommand

from api_clients import CrossroadsApiClient
from campaigns.models import CrossroadsCampaign

from metrics.models import CrossroadsCampaignMetrics


class Command(BaseCommand):
    help = "Load crossroads campaigns' metrics to the database"

    def add_arguments(self, parser):
        parser.add_argument("config", type=str)

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.api_client = CrossroadsApiClient(options["config"])

        data = self.api_client.request_campaigns_report(self.datetime, self.datetime)

        campaigns = []
        metrics = []
        for row in data:
            campaign = CrossroadsCampaign(
                id=row["campaign_id"],
                name=row["campaign__name"],
            )
            campaigns.append(campaign)
            metrics.append(
                CrossroadsCampaignMetrics(
                    campaign=campaign,
                    date=self.datetime.date(),
                    revenue=row["revenue"],
                    rpc=row["rpc"],
                    rpv=row["rpv"],
                    total_visitors=row["total_visitors"],
                    filtered_visitors=row["filtered_visitors"],
                    lander_visitors=row["lander_visitors"],
                    lander_searches=row["lander_searches"],
                    revenue_events=row["revenue_events"],
                )
            )

        campaigns_results = CrossroadsCampaign.objects.bulk_create(
            campaigns,
            update_conflicts=True,
            unique_fields=["id"],
            update_fields=["name"],
        )

        metrics_results = CrossroadsCampaignMetrics.objects.bulk_create(
            metrics,
            update_conflicts=True,
            unique_fields=["campaign", "date"],
            update_fields=[
                "date",
                "revenue",
                "rpc",
                "rpv",
                "total_visitors",
                "filtered_visitors",
                "lander_visitors",
                "lander_searches",
                "revenue_events",
            ],
        )
