# Generated by Django 5.0.1 on 2024-04-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="email",
        ),
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]