# Generated by Django 3.1.4 on 2021-01-09 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210109_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.IntegerField(),
        ),
    ]
