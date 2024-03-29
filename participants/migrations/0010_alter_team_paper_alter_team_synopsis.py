# Generated by Django 4.1.7 on 2023-04-02 18:45

from django.db import migrations, models
import participants.models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0009_remove_team_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="paper",
            field=models.FileField(
                blank=True, default="", upload_to=participants.models.paper_name
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="synopsis",
            field=models.FileField(
                blank=True, default="", upload_to=participants.models.synopsis_name
            ),
        ),
    ]
