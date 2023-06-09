# Generated by Django 4.1.5 on 2023-02-03 19:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rideshareapp", "0003_remove_ride_sharer_num"),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="sharer_num",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.IntegerField(), size=None
                ),
                default=[],
                size=None,
            ),
        ),
    ]
