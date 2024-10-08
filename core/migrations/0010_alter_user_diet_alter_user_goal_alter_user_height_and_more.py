# Generated by Django 5.1 on 2024-08-28 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_user_diet_alter_user_goal_alter_user_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='diet',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='goal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.IntegerField(blank=True, null=True, verbose_name='height in cm'),
        ),
        migrations.AlterField(
            model_name='user',
            name='imc',
            field=models.FloatField(blank=True, null=True, verbose_name='imc'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='weekly_exercise_hours',
            field=models.IntegerField(blank=True, null=True, verbose_name='weekly exercise hours'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name='weight in kg'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
