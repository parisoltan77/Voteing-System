# Generated by Django 3.1.6 on 2021-02-08 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_auto_20210208_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='images/', verbose_name='Candidate Pic'),
        ),
    ]
