# Generated by Django 4.1.7 on 2023-03-06 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0005_alter_participant_year_of_study"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="mobile",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="participant",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Others")], max_length=10
            ),
        ),
    ]
