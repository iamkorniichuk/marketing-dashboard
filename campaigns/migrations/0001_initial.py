# Generated by Django 4.2.10 on 2024-04-03 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrossroadsCampaign",
            fields=[
                (
                    "id",
                    models.CharField(max_length=128, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name": "Crossroads Campaign",
                "verbose_name_plural": "Crossroads",
            },
        ),
        migrations.CreateModel(
            name="TiktokBusinessAdvertiser",
            fields=[
                (
                    "id",
                    models.CharField(max_length=128, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TiktokBusinessCampaign",
            fields=[
                (
                    "id",
                    models.CharField(max_length=128, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=256)),
                (
                    "advertiser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="campaigns",
                        to="campaigns.tiktokbusinessadvertiser",
                    ),
                ),
            ],
            options={
                "verbose_name": "Tiktok Business Campaign",
                "verbose_name_plural": "Tiktok Business",
            },
        ),
        migrations.CreateModel(
            name="CrossroadsToTiktokBusinessIdentifiers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "crossroads",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="identifiers",
                        to="campaigns.crossroadscampaign",
                    ),
                ),
                (
                    "tiktok_business",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="identifiers",
                        to="campaigns.tiktokbusinesscampaign",
                    ),
                ),
            ],
        ),
    ]