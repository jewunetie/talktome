# Generated by Django 4.2.9 on 2024-01-13 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entries", "0002_alter_entry_options_entry_positive_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="entry",
            name="find_pattern",
            field=models.TextField(blank=True, null=True),
        ),
    ]
