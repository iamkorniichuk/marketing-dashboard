# Generated by Django 4.2.10 on 2024-03-19 17:07

from django.db import migrations


def create_merged_campaign_metrics(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    TempMetrics = apps.get_model("campaigns", "MergedCampaign")

    TiktokBusinessMetrics = apps.get_model("metrics", "TiktokBusinessCampaignMetrics")
    CrossroadsMetrics = apps.get_model("metrics", "CrossroadsCampaignMetrics")

    Metrics = apps.get_model("metrics", "CampaignMetrics")
    instances = []
    for obj in TempMetrics.objects.using(db_alias).all():
        crossroads_metrics = CrossroadsMetrics.objects.get(
            campaign=obj.crossroads.identifier, date=obj.crossroads.date
        )
        tiktok_business_metrics = TiktokBusinessMetrics.objects.get(
            campaign=obj.tiktok_business.identifier, date=obj.tiktok_business.date
        )
        instances.append(
            Metrics(
                crossroads_metrics=crossroads_metrics,
                tiktok_business_metrics=tiktok_business_metrics,
                date=obj.date,
            )
        )
    Metrics.objects.using(db_alias).bulk_create(instances, ignore_conflicts=True)


class Migration(migrations.Migration):

    dependencies = [
        ("metrics", "0003_campaignmetrics_and_more"),
    ]

    operations = [
        migrations.RunPython(create_merged_campaign_metrics),
    ]
