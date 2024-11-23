# Generated by Django 4.1.1 on 2024-11-21 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_room_interested_users_alter_room_interested_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleanliness', models.IntegerField(choices=[(1, 'Very Neat'), (2, 'Moderately Clean'), (3, 'Relaxed')])),
                ('noise_level', models.IntegerField(choices=[(1, 'Quiet'), (2, 'Moderate'), (3, 'Loud')])),
                ('guests_frequency', models.IntegerField(choices=[(1, 'Rarely'), (2, 'Sometimes'), (3, 'Often')])),
                ('early_bird', models.BooleanField(default=False)),
                ('night_owl', models.BooleanField(default=False)),
                ('smoking_tolerance', models.BooleanField(default=False)),
                ('pet_friendly', models.BooleanField(default=False)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='match_preferences', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]