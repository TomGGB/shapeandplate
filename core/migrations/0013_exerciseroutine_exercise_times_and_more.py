# Generated by Django 5.1.1 on 2024-09-15 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_exerciseroutine_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseroutine',
            name='exercise_times',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='exerciseroutine',
            name='progress',
            field=models.JSONField(default=dict),
        ),
    ]
