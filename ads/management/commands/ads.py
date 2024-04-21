from django.core.management.base import BaseCommand

from ads.generators import generate_ads


class Command(BaseCommand):
    help = "Load tiktok ads to the database"

    def handle(self, *args, **options):
        generate_ads()
