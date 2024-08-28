# Generated by Django 5.1 on 2024-08-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='goal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='imc',
            field=models.FloatField(blank=True, null=True, verbose_name='imc'),
        ),
    ]