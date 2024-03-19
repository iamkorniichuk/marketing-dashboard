from datetime import datetime

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from api_clients import TiktokBusinessApiClient, CrossroadsApiClient
from campaigns.models import (
    TempTiktokBusinessCampaign,
    TempCrossroadsCampaign,
    CrossroadsToTiktokBusinessIdentifiers,
    MergedCampaign,
)


class Command(BaseCommand):
    help = "Save campaigns to a current database"

    def add_arguments(self, parser):
        parser.add_argument("crossroads", type=str)
        parser.add_argument("tiktok", type=str)

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.crossroads_api_client = CrossroadsApiClient(options["crossroads"])
        self.tiktok_business_api_client = TiktokBusinessApiClient(options["tiktok"])

        crossroads_campaigns = self.gather_crossroads_campaigns()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(crossroads_campaigns)} Crossroads Campaigns"
            )
        )
        tiktok_business_campaigns = self.gather_tiktok_business_campaigns()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(tiktok_business_campaigns)} Tiktok Business Campaigns"
            )
        )
        merged_campaigns = self.gather_merged_campaigns(tiktok_business_campaigns)
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(merged_campaigns)} Merged Campaigns")
        )

    # TODO: Optimize 'cause there are too many Tiktok Business Campaigns
    def gather_merged_campaigns(self, tiktok_business_campaigns):
        objs = []
        for campaign in tiktok_business_campaigns:
            if not CrossroadsToTiktokBusinessIdentifiers.objects.filter(
                tiktok_business=campaign.identifier
            ).exists():
                crossroads_ids = self.gather_crossroads_ids(campaign.advertiser_id)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created {len(crossroads_ids)} Crossroads To TiktokBusiness Identifiers for {campaign.advertiser_id} Advertiser"
                    )
                )

            try:
                ids = CrossroadsToTiktokBusinessIdentifiers.objects.get(
                    tiktok_business=campaign.identifier
                )
                tiktok_business = TempTiktokBusinessCampaign.objects.get(
                    identifier=ids.tiktok_business,
                    date=self.datetime.date(),
                )
                crossroads = TempCrossroadsCampaign.objects.get(
                    identifier=ids.crossroads,
                    date=self.datetime.date(),
                )
                objs.append(
                    MergedCampaign(
                        tiktok_business=tiktok_business, crossroads=crossroads
                    )
                )
            except ObjectDoesNotExist:
                pass
        return MergedCampaign.objects.bulk_create(objs, ignore_conflicts=True)

    def gather_crossroads_ids(self, advertiser_id):
        data = self.tiktok_business_api_client.request_crossroads_id(advertiser_id)

        objs = []
        for row in data:
            objs.append(
                CrossroadsToTiktokBusinessIdentifiers(
                    tiktok_business=row["campaign_id"],
                    crossroads=row["cr_campaign_id"],
                )
            )

        return CrossroadsToTiktokBusinessIdentifiers.objects.bulk_create(
            objs, ignore_conflicts=True
        )

    def gather_crossroads_campaigns(self):
        data = self.crossroads_api_client.request_campaigns_report(
            self.datetime, self.datetime
        )

        campaigns = []
        for row in data:
            campaigns.append(
                TempCrossroadsCampaign(
                    identifier=row["campaign_id"],
                    name=row["campaign__name"],
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

        return TempCrossroadsCampaign.objects.bulk_create(
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

    def gather_tiktok_business_campaigns(self):
        advertisers = self.tiktok_business_api_client.request_advertisers()

        campaigns = []
        for advertiser in advertisers:
            data = self.tiktok_business_api_client.request_campaigns_report(
                advertiser["advertiser_id"],
                self.datetime,
                self.datetime,
            )

            for row in data:
                campaigns.append(
                    TempTiktokBusinessCampaign(
                        identifier=row["campaign_id"],
                        name=row["campaign_name"],
                        advertiser_id=row["advertiser_id"],
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

        return TempTiktokBusinessCampaign.objects.bulk_create(
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
