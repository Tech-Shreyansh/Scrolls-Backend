# Generated by Django 4.1.7 on 2023-03-05 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "participants",
            "0004_alter_participant_college_alter_participant_gender_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="year_of_study",
            field=models.PositiveIntegerField(),
        ),
    ]
