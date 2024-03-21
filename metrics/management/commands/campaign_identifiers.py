from datetime import datetime
from paths import TIKTOK_BUSINESS_CONFIG

from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from api_clients import TiktokBusinessApiClient
from campaigns.models import (
    TiktokBusinessCampaign,
    CrossroadsCampaign,
    CrossroadsToTiktokBusinessIdentifiers,
)


class Command(BaseCommand):
    help = "Create identifiers to relate Crossroads to Tiktok Business campaigns"

    def add_arguments(self, parser):
        parser.add_argument(
            "-cfg",
            "--config",
            type=str,
            default=TIKTOK_BUSINESS_CONFIG,
        )

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        self.api_client = TiktokBusinessApiClient(options["config"])
        incomplete_campaigns = TiktokBusinessCampaign.objects.filter(
            ~Exists(
                CrossroadsToTiktokBusinessIdentifiers.objects.filter(
                    tiktok_business=OuterRef("id")
                )
            )
        )
        advertiser_id_values = incomplete_campaigns.values_list(
            "advertiser_id", flat=True
        ).distinct()

        objs = []
        for advertiser_id in advertiser_id_values:
            data = self.api_client.request_crossroads_id(advertiser_id)
            for row in data:
                tiktok_business = TiktokBusinessCampaign.objects.filter(
                    id=row["campaign_id"]
                ).first()
                crossroads = CrossroadsCampaign.objects.filter(
                    id=row["cr_campaign_id"]
                ).first()
                if tiktok_business and crossroads:
                    objs.append(
                        CrossroadsToTiktokBusinessIdentifiers(
                            tiktok_business=tiktok_business,
                            crossroads=crossroads,
                        )
                    )

        identifiers = CrossroadsToTiktokBusinessIdentifiers.objects.bulk_create(
            objs, ignore_conflicts=True
        )
