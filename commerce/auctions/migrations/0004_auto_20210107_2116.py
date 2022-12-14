# Generated by Django 3.1.4 on 2021-01-08 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_lis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('bid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=200)),
                ('user', models.CharField(max_length=20)),
                ('listingid', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
                ('time', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.AlterField(
            model_name='lis',
            name='link',
            field=models.CharField(blank=True, default=None, max_length=150),
        ),
    ]
