# Generated by Django 5.0.3 on 2024-03-17 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("keywords", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="crossroadskeyword",
            constraint=models.UniqueConstraint(
                fields=("campaign_id", "lander_keyword", "date"),
                name="crossroads_unique_keyword_for_date",
            ),
        ),
    ]