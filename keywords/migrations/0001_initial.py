# Generated by Django 4.2.10 on 2024-04-03 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BaseKeyword",
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
                ("text", models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserKeyword",
            fields=[
                (
                    "basekeyword_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="keywords.basekeyword",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Keyword",
                "verbose_name_plural": "User",
            },
            bases=("keywords.basekeyword",),
        ),
        migrations.CreateModel(
            name="ChatGptKeyword",
            fields=[
                (
                    "basekeyword_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="keywords.basekeyword",
                    ),
                ),
                (
                    "based_on",
                    models.ManyToManyField(
                        related_name="chat_gpt_keywords", to="keywords.basekeyword"
                    ),
                ),
            ],
            options={
                "verbose_name": "ChatGPT Keyword",
                "verbose_name_plural": "ChatGPT",
            },
            bases=("keywords.basekeyword",),
        ),
    ]