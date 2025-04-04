# Generated by Django 5.1.7 on 2025-03-30 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('capacity', models.IntegerField(default=10)),
                ('availability', models.BooleanField(default=True)),
                ('operating_hours', models.CharField(max_length=50)),
            ],
        ),
    ]
