# Generated by Django 4.1.7 on 2023-03-09 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0009_team"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="is_registered",
            field=models.BooleanField(default=False),
        ),
    ]
