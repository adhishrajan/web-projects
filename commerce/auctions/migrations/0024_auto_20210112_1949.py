# Generated by Django 3.1.4 on 2021-01-13 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auto_20210112_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='id',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_id',
            field=models.IntegerField(default=None, primary_key=True, serialize=False),
        ),
    ]
