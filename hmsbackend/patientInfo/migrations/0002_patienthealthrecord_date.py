# Generated by Django 5.0.7 on 2024-07-16 07:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patientInfo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="patienthealthrecord",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 7, 16, 7, 59, 46, 772036, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
    ]
