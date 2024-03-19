# Generated by Django 4.2.10 on 2024-03-19 10:55

from typing import Iterable
from django.db import migrations, models


def sqlite_distinct(queryset, distinct_on: Iterable[str], values: Iterable[str]):
    values_kwargs = {}
    for field in values:
        values_kwargs[field] = models.Min(field)

    return queryset.values(*distinct_on).distinct().annotate(**values_kwargs)


def create_tiktok_business_campaigns(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    TempCampaign = apps.get_model("campaigns", "TempTiktokBusinessCampaign")

    Advertiser = apps.get_model("campaigns", "TiktokBusinessAdvertiser")
    advertisers = []
    for unique_id in (
        TempCampaign.objects.using(db_alias)
        .values_list("advertiser_id", flat=True)
        .distinct()
    ):
        advertisers.append(Advertiser(id=unique_id))
    Advertiser.objects.using(db_alias).bulk_create(advertisers, ignore_conflicts=True)

    Campaign = apps.get_model("campaigns", "TiktokBusinessCampaign")
    campaigns = []
    for values in sqlite_distinct(
        TempCampaign.objects.using(db_alias), ["identifier"], ["name", "advertiser_id"]
    ):
        campaigns.append(
            Campaign(
                id=values["identifier"],
                name=values["name"],
                advertiser_id=values["advertiser_id"],
            )
        )
    Campaign.objects.using(db_alias).bulk_create(campaigns, ignore_conflicts=True)


def create_crossroads_campaigns(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    TempCampaign = apps.get_model("campaigns", "TempCrossroadsCampaign")
    Campaign = apps.get_model("campaigns", "CrossroadsCampaign")

    campaigns = []
    for values in sqlite_distinct(
        TempCampaign.objects.using(db_alias), ["identifier"], ["name"]
    ):
        campaigns.append(Campaign(id=values["identifier"], name=values["name"]))
    Campaign.objects.using(db_alias).bulk_create(campaigns, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0010_crossroadscampaign_tiktokbusinessadvertiser_and_more"),
    ]

    operations = [
        migrations.RunPython(create_tiktok_business_campaigns),
        migrations.RunPython(create_crossroads_campaigns),
    ]