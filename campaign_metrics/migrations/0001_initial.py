# Generated by Django 4.2.10 on 2024-04-03 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TiktokBusinessCampaignMetrics",
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
                ("date", models.DateField()),
                ("video_play_actions", models.IntegerField()),
                ("video_watched_2s", models.IntegerField()),
                ("video_watched_6s", models.IntegerField()),
                ("video_views_p25", models.IntegerField()),
                ("video_views_p50", models.IntegerField()),
                ("video_views_p75", models.IntegerField()),
                ("video_views_p100", models.IntegerField()),
                ("cost_per_conversion", models.FloatField()),
                ("cpc", models.FloatField()),
                ("ctr", models.FloatField()),
                ("clicks", models.IntegerField()),
                ("spend", models.FloatField()),
                ("conversion", models.FloatField()),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="campaign_metrics",
                        to="campaigns.tiktokbusinesscampaign",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CrossroadsCampaignMetrics",
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
                ("date", models.DateField()),
                ("revenue", models.FloatField()),
                ("rpc", models.FloatField()),
                ("rpv", models.FloatField()),
                ("total_visitors", models.IntegerField()),
                ("filtered_visitors", models.IntegerField()),
                ("lander_visitors", models.IntegerField()),
                ("lander_searches", models.IntegerField()),
                ("revenue_events", models.IntegerField()),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="campaign_metrics",
                        to="campaigns.crossroadscampaign",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CampaignMetrics",
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
                ("date", models.DateField()),
                (
                    "crossroads_metrics",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="all_campaign_metrics",
                        to="campaign_metrics.crossroadscampaignmetrics",
                    ),
                ),
                (
                    "tiktok_business_metrics",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="all_campaign_metrics",
                        to="campaign_metrics.tiktokbusinesscampaignmetrics",
                    ),
                ),
            ],
            options={
                "verbose_name": "Full Metrics",
                "verbose_name_plural": "Full",
            },
        ),
        migrations.CreateModel(
            name="ProxyCampaignMetrics",
            fields=[],
            options={
                "verbose_name": "Short Metrics",
                "verbose_name_plural": "Short",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("campaign_metrics.campaignmetrics",),
        ),
        migrations.AddConstraint(
            model_name="tiktokbusinesscampaignmetrics",
            constraint=models.UniqueConstraint(
                fields=("campaign", "date"),
                name="tiktok_business_unique_metrics_for_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="crossroadscampaignmetrics",
            constraint=models.UniqueConstraint(
                fields=("campaign", "date"), name="crossroads_unique_metrics_for_date"
            ),
        ),
        migrations.AddConstraint(
            model_name="campaignmetrics",
            constraint=models.UniqueConstraint(
                fields=("tiktok_business_metrics", "crossroads_metrics", "date"),
                name="unique_campaign_metrics_for_date",
            ),
        ),
    ]
