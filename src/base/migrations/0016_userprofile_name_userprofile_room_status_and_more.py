# Generated by Django 5.1.3 on 2024-11-24 23:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0015_remove_userprofile_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="name",
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="room_status",
            field=models.CharField(
                choices=[
                    ("offering", "Offering"),
                    ("available", "Available"),
                    ("occupied", "Occupied"),
                ],
                default="available",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="userprofile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
