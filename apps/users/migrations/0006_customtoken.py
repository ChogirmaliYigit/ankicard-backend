# Generated by Django 5.0.1 on 2024-04-25 06:02

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_user_full_name_alter_word_back_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomToken",
            fields=[
                (
                    "key",
                    models.CharField(
                        max_length=40,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 5, 25, 11, 2, 51, 110126)
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "db_table": "custom_tokens",
            },
        ),
    ]