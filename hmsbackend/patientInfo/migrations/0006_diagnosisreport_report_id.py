# Generated by Django 5.0.7 on 2024-07-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "patientInfo",
            "0005_remove_diagnosisreport_user_diagnosisreport_user_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="diagnosisreport",
            name="report_id",
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
