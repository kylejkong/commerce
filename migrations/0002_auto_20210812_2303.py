# Generated by Django 3.2.6 on 2021-08-12 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
            preserve_default=False,
        ),
    ]