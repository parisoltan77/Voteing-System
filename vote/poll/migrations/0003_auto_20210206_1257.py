# Generated by Django 3.1.6 on 2021-02-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20210206_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='end_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='start_at',
            field=models.DateTimeField(null=True),
        ),
    ]
