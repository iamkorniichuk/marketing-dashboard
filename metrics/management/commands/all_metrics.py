from django.core.management import call_command, BaseCommand
from paths import CROSSROADS_CONFIG, TIKTOK_BUSINESS_CONFIG

from metrics.management.commands import (
    campaign_identifiers,
    crossroads_campaign_metrics,
    merge_campaign_metrics,
    tiktok_business_campaign_metrics,
    crossroads_keyword_metrics,
)


class Command(BaseCommand):
    help = "Load all current metrics to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "-cr_cfg",
            "--crossroads_config",
            dest="crossroads_config",
            type=str,
            default=CROSSROADS_CONFIG,
        )
        parser.add_argument(
            "-tt_b_cfg",
            "--tiktok-business_config",
            dest="tiktok_business_config",
            type=str,
            default=TIKTOK_BUSINESS_CONFIG,
        )

    def handle(self, *args, **options):
        call_command(
            crossroads_campaign_metrics.Command(),
            config=options["crossroads_config"],
        )
        call_command(
            tiktok_business_campaign_metrics.Command(),
            config=options["tiktok_business_config"],
        )

        call_command(
            campaign_identifiers.Command(),
            config=options["tiktok_business_config"],
        )
        call_command(merge_campaign_metrics.Command())

        call_command(
            crossroads_keyword_metrics.Command(),
            config=options["crossroads_config"],
        )
