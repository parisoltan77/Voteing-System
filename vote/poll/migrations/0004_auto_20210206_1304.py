# Generated by Django 3.1.6 on 2021-02-06 13:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_auto_20210206_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='end_at',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='start_at',
        ),
        migrations.AddField(
            model_name='position',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 13, 4, 9, 473717, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='position',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 6, 13, 4, 9, 473693, tzinfo=utc)),
        ),
    ]
