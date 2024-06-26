from datetime import datetime

from django.core.management.base import BaseCommand

from api_clients import TiktokBusinessApiClient
from campaigns.models import TiktokBusinessCampaign, TiktokAdvertiser

from campaign_metrics.models import TiktokBusinessCampaignMetrics


class Command(BaseCommand):
    help = "Load tiktok business campaigns' metrics to the database"

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.api_client = TiktokBusinessApiClient()
        self.create_advertisers()
        self.create_metrics()

    def create_advertisers(self):
        data = self.api_client.request_advertisers()

        advertisers = []
        for row in data:
            obj = TiktokAdvertiser(id=row["advertiser_id"])
            advertisers.append(obj)

        results = TiktokAdvertiser.objects.bulk_create(
            advertisers,
            ignore_conflicts=True,
        )
        return results

    def create_metrics(self):
        for advertiser_id in TiktokAdvertiser.objects.values_list("id", flat=True):
            data = self.api_client.request_campaigns_report(
                advertiser_id,
                self.datetime,
                self.datetime,
            )

            campaigns = []
            metrics = []
            for row in data:
                campaign = TiktokBusinessCampaign(
                    id=row["campaign_id"],
                    name=row["campaign_name"],
                    advertiser_id=row["advertiser_id"],
                )
                campaigns.append(campaign)

                metrics.append(
                    TiktokBusinessCampaignMetrics(
                        campaign=campaign,
                        date=self.datetime.date(),
                        video_play_actions=row["video_play_actions"],
                        video_watched_2s=row["video_watched_2s"],
                        video_watched_6s=row["video_watched_6s"],
                        video_views_p25=row["video_views_p25"],
                        video_views_p50=row["video_views_p50"],
                        video_views_p75=row["video_views_p75"],
                        video_views_p100=row["video_views_p100"],
                        cost_per_conversion=row["cost_per_conversion"],
                        cpc=row["cpc"],
                        ctr=row["ctr"],
                        clicks=row["clicks"],
                        spend=row["spend"],
                        conversion=row["conversion"],
                    )
                )

            campaigns_results = TiktokBusinessCampaign.objects.bulk_create(
                campaigns,
                update_conflicts=True,
                unique_fields=["id"],
                update_fields=["name", "advertiser_id"],
            )

            metrics_results = TiktokBusinessCampaignMetrics.objects.bulk_create(
                metrics,
                update_conflicts=True,
                unique_fields=["campaign", "date"],
                update_fields=[
                    "video_play_actions",
                    "video_watched_2s",
                    "video_watched_6s",
                    "video_views_p25",
                    "video_views_p50",
                    "video_views_p75",
                    "video_views_p100",
                    "cost_per_conversion",
                    "cpc",
                    "ctr",
                    "clicks",
                    "spend",
                    "conversion",
                ],
            )
