# Generated by Django 4.2.10 on 2024-03-18 09:27

from django.db import migrations


def populate_date(apps, schema_editor):
    MergedCampaign = apps.get_model("campaigns", "MergedCampaign")
    db_alias = schema_editor.connection.alias
    for obj in MergedCampaign.objects.using(db_alias).all():
        obj.date = obj.crossroads.date
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0004_mergedcampaign_date"),
    ]

    operations = [
        migrations.RunPython(populate_date),
    ]
