# Generated by Django 4.1.7 on 2023-03-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0003_team_paper_team_synopsis"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="paper",
            field=models.FileField(default="", upload_to="media"),
        ),
        migrations.AlterField(
            model_name="team",
            name="synopsis",
            field=models.FileField(default="", upload_to="media"),
        ),
    ]
