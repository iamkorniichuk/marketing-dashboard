# Generated by Django 5.0.3 on 2024-03-17 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CrossroadsKeyword",
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
                ("campaign_id", models.CharField(max_length=128)),
                ("lander_keyword", models.CharField(max_length=128)),
                ("clicks", models.IntegerField()),
                ("date", models.DateField()),
            ],
        ),
    ]
