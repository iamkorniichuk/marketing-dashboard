from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from campaigns.models import CrossroadsToTiktokBusinessIdentifiers

from metrics.models import (
    TiktokBusinessCampaignMetrics,
    CrossroadsCampaignMetrics,
    CampaignMetrics,
)


class Command(BaseCommand):
    help = "Merge tiktok business campaigns' metrics with corresponding crossroads' one"

    def handle(self, *args, **options):
        self.datetime = datetime.now()

        incomplete_tiktok_business_metrics = (
            TiktokBusinessCampaignMetrics.objects.filter(
                ~Exists(
                    CampaignMetrics.objects.filter(
                        tiktok_business_metrics=OuterRef("pk")
                    )
                ),
                date=self.datetime.date(),
            ).all()
        )

        campaign_metrics = []
        for tiktok_business_metrics in incomplete_tiktok_business_metrics:
            identifiers = CrossroadsToTiktokBusinessIdentifiers.objects.filter(
                tiktok_business=tiktok_business_metrics.campaign
            ).first()
            if identifiers:
                crossroads_metrics = CrossroadsCampaignMetrics.objects.filter(
                    campaign=identifiers.crossroads, date=self.datetime.date()
                ).first()
                if crossroads_metrics:
                    campaign_metrics.append(
                        CampaignMetrics(
                            tiktok_business_metrics=tiktok_business_metrics,
                            crossroads_metrics=crossroads_metrics,
                        )
                    )

        results = CampaignMetrics.objects.bulk_create(
            campaign_metrics, ignore_conflicts=True
        )
