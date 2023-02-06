# Generated by Django 4.1.5 on 2023-02-03 19:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rideshareapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
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
