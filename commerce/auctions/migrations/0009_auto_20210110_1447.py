# Generated by Django 3.1.4 on 2021-01-10 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210109_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='listingid',
            new_name='listing_id',
        ),
    ]
