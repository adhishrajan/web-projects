# Generated by Django 3.1.4 on 2021-01-11 19:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210111_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lis',
            name='watchers',
            field=models.ManyToManyField(blank=True, default=None, related_name='watched_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
