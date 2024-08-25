# Generated by Django 5.1 on 2024-08-25 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0007_alter_usuario_options_alter_usuario_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='apellidos',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
