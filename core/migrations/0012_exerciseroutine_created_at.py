# Generated by Django 5.1.1 on 2024-09-15 17:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_gym_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseroutine',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
