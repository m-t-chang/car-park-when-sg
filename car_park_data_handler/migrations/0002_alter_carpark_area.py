# Generated by Django 4.0.2 on 2022-02-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_park_data_handler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpark',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
