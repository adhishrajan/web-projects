# Generated by Django 3.1.4 on 2021-01-13 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_auto_20210112_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
