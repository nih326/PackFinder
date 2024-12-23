# Generated by Django 4.1.1 on 2024-11-19 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_merge_20241119_1216"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "room_status",
                    models.CharField(
                        choices=[
                            ("offering", "Offering"),
                            ("available", "Available"),
                            ("occupied", "Occupied"),
                        ],
                        default="available",
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
