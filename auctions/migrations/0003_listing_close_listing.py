# Generated by Django 3.2.6 on 2021-08-13 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210812_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='close_listing',
            field=models.BooleanField(default=False),
        ),
    ]