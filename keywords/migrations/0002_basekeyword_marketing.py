# Generated by Django 4.2.10 on 2024-04-06 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("keywords", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="basekeyword",
            name="marketing",
            field=models.CharField(
                choices=[
                    ("", ""),
                    ("B2C", "Business To Customer"),
                    ("B2B", "Business To Business"),
                ],
                default="",
                blank=True,
                max_length=64,
            ),
        ),
    ]
