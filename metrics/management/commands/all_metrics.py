from django.core.management import call_command, BaseCommand

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
        parser.add_argument("crossroads", type=str)
        parser.add_argument("tiktok", type=str)

    def handle(self, *args, **options):
        call_command(crossroads_campaign_metrics.Command(), options["crossroads"])
        call_command(tiktok_business_campaign_metrics.Command(), options["tiktok"])

        call_command(campaign_identifiers.Command(), options["tiktok"])
        call_command(merge_campaign_metrics.Command())

        call_command(crossroads_keyword_metrics.Command(), options["crossroads"])
