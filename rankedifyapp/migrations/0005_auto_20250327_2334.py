# Generated by Django 2.2.28 on 2025-03-27 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankedifyapp', '0004_remove_profile_username_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='spotify_username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
