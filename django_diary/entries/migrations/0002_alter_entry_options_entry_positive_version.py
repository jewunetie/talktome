# Generated by Django 4.2.1 on 2024-01-13 21:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entries", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={"verbose_name_plural": "Entries"},
        ),
        migrations.AddField(
            model_name="entry",
            name="positive_version",
            field=models.TextField(blank=True, null=True),
        ),
    ]
