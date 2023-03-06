# Generated by Django 4.1.7 on 2023-03-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0007_alter_participant_mobile"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="is_ambassador",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="participant",
            name="referral_code",
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
