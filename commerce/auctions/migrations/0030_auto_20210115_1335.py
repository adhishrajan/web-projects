# Generated by Django 3.1.4 on 2021-01-15 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0029_auto_20210114_1452'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ClosedBid',
            new_name='ClosedLis',
        ),
    ]
