# Generated by Django 5.0.1 on 2024-04-25 06:05

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_customtoken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customtoken",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 25, 11, 5, 5, 445689)
            ),
        ),
    ]
