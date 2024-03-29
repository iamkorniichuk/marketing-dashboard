# Generated by Django 4.2.10 on 2024-03-20 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "campaigns",
            "0013_alter_crossroadstotiktokbusinessidentifiers_options_and_more",
        ),
        ("metrics", "0006_alter_campaignmetrics_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaignmetrics",
            name="crossroads_metrics",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="all_campaign_metrics",
                to="metrics.crossroadscampaignmetrics",
            ),
        ),
        migrations.AlterField(
            model_name="campaignmetrics",
            name="tiktok_business_metrics",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="all_campaign_metrics",
                to="metrics.tiktokbusinesscampaignmetrics",
            ),
        ),
        migrations.AlterField(
            model_name="crossroadscampaignmetrics",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="campaign_metrics",
                to="campaigns.crossroadscampaign",
            ),
        ),
        migrations.AlterField(
            model_name="crossroadskeywordmetrics",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="keyword_metrics",
                to="campaigns.crossroadscampaign",
            ),
        ),
        migrations.AlterField(
            model_name="tiktokbusinesscampaignmetrics",
            name="campaign",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="campaign_metrics",
                to="campaigns.tiktokbusinesscampaign",
            ),
        ),
    ]
