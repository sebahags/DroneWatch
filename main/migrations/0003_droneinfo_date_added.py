# Generated by Django 4.1.5 on 2023-01-18 12:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_pilotname_droneinfo_pilotfirstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='droneinfo',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]