# Generated by Django 4.1.7 on 2023-03-09 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("participants", "0012_team_domain_team_leader_id_team_member_2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="participant",
            name="is_registered",
        ),
    ]
