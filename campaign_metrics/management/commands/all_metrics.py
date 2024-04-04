from django.core.management import call_command, BaseCommand

from campaign_metrics.management.commands import (
    campaign_identifiers,
    crossroads_campaign_metrics,
    merge_campaign_metrics,
    tiktok_business_campaign_metrics,
)

from keyword_metrics.management.commands import crossroads_keyword_metrics


class Command(BaseCommand):
    help = "Load all current metrics to the database"

    def handle(self, *args, **options):
        call_command(
            crossroads_campaign_metrics.Command(),
        )
        call_command(
            tiktok_business_campaign_metrics.Command(),
        )

        call_command(
            campaign_identifiers.Command(),
        )
        call_command(merge_campaign_metrics.Command())

        call_command(
            crossroads_keyword_metrics.Command(),
        )
