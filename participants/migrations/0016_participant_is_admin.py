# Generated by Django 4.1.7 on 2023-03-09 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "participants",
            "0015_alter_participant_college_alter_participant_course_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
    ]
