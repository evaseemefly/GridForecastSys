# Generated by Django 2.0.4 on 2018-08-02 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StormTide', '0003_auto_20180731_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stormtideinfo',
            name='tdate',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]