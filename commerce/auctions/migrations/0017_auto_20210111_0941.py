# Generated by Django 3.1.4 on 2021-01-11 15:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210111_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lis',
            name='watchers',
        ),
        migrations.AddField(
            model_name='lis',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watched_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]