# Generated by Django 4.2.10 on 2024-03-23 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("keywords", "0006_googleadskeyword"),
        ("metrics", "0008_googleadshistoricalkeywordmetrics_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoogleAdsForecastKeywordMetrics",
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
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("impressions", models.FloatField()),
                ("partners_impressions", models.FloatField()),
                ("ctr", models.FloatField()),
                ("partners_ctr", models.FloatField()),
                ("average_cpc", models.FloatField()),
                ("partners_average_cpc", models.FloatField()),
                ("clicks", models.FloatField()),
                ("partners_clicks", models.FloatField()),
                ("cost", models.FloatField()),
                ("partners_cost", models.FloatField()),
                ("conversions", models.FloatField()),
                ("partners_conversions", models.FloatField()),
                ("conversion_rate", models.FloatField()),
                ("partners_conversion_rate", models.FloatField()),
                ("average_cpa", models.FloatField()),
                ("partners_average_cpa", models.FloatField()),
                (
                    "keyword",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="forecast_metrics",
                        to="keywords.googleadskeyword",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Google Ads Forecast Keyword Metrics",
            },
        ),
        migrations.AddConstraint(
            model_name="googleadsforecastkeywordmetrics",
            constraint=models.UniqueConstraint(
                fields=("keyword", "start_date", "end_date"),
                name="unique_google_ads_forecast_keyword_metrics_for_date",
            ),
        ),
    ]
