# Generated by Django 4.2.10 on 2024-03-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaigns", "0003_crossroadstotiktokbusinessidentifiers"),
    ]

    operations = [
        migrations.AddField(
            model_name="mergedcampaign",
            name="date",
            field=models.DateField(null=True),
        ),
    ]
