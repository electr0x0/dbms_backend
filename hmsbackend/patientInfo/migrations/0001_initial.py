# Generated by Django 5.0.7 on 2024-07-13 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientHealthRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("blood_type", models.CharField(max_length=3)),
                ("bmi", models.FloatField()),
                ("height", models.FloatField()),
                ("weight", models.FloatField()),
                ("blood_pressure", models.CharField(max_length=7)),
                ("heart_rate", models.IntegerField()),
                ("cholesterol_level", models.FloatField()),
                ("sugar_level", models.FloatField()),
                (
                    "p_user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
