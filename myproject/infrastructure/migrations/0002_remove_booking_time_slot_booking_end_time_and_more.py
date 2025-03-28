# Generated by Django 5.1.7 on 2025-03-25 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='booking',
            name='end_time',
            field=models.DateTimeField(default="2025-03-25 23:59:59"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='start_time',
            field=models.DateTimeField(default='23:59:59'),
            preserve_default=False,
        ),
    ]
