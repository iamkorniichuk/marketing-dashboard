from datetime import datetime

from django.core.management.base import BaseCommand

from api_clients import TiktokBusinessApiClient, CrossroadsApiClient
from campaigns.models import TiktokBusinessCampaign, CrossroadsCampaign, MergedCampaign


class Command(BaseCommand):
    help = "Save campaigns to a current database"

    def add_arguments(self, parser):
        parser.add_argument("crossroads", type=str)
        parser.add_argument("tiktok", type=str)

    def handle(self, *args, **options):
        crossroads_campaigns = self.gather_crossroads_campaigns(options["crossroads"])
        tiktok_business_campaigns = self.gather_tiktok_business_campaigns(
            options["tiktok"]
        )

    def gather_crossroads_campaigns(self, config):
        api_client = CrossroadsApiClient(config)

        today = datetime.now()
        data = api_client.request_campaigns_report(today, today)

        campaigns = []
        for row in data:
            campaigns.append(
                CrossroadsCampaign(
                    identifier=row["campaign_id"],
                    name=row["campaign__name"],
                    date=today.date(),
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

        return CrossroadsCampaign.objects.bulk_create(
            campaigns,
            update_conflicts=True,
            unique_fields=["identifier", "date"],
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

    def gather_tiktok_business_campaigns(self, config):
        api_client = TiktokBusinessApiClient(config)

        today = datetime.now()
        advertisers = api_client.request_advertisers()

        campaigns = []
        for advertiser in advertisers:
            data = api_client.request_campaigns_report(
                advertiser["advertiser_id"],
                today,
                today,
            )

            for row in data:
                campaigns.append(
                    TiktokBusinessCampaign(
                        identifier=row["campaign_id"],
                        name=row["campaign_name"],
                        advertiser_id=row["advertiser_id"],
                        date=today.date(),
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

        return TiktokBusinessCampaign.objects.bulk_create(
            campaigns,
            update_conflicts=True,
            unique_fields=["identifier", "date"],
            update_fields=[
                "name",
                "advertiser_id",
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
