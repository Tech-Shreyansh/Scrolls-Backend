# Generated by Django 4.1.7 on 2023-03-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0013_remove_participant_is_registered"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="year_of_study",
            field=models.PositiveIntegerField(null=True),
        ),
    ]
