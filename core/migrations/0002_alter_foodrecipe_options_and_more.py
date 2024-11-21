# core/migrations/0002_alter_foodrecipe_options_and_more.py

from django.db import migrations, models
from django.utils.timezone import now  # Importa 'now'

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodrecipe',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='foodrecipe',
            old_name='recipe',
            new_name='plan_semanal',
        ),
        migrations.AddField(
            model_name='foodrecipe',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=now), 
            preserve_default=False,
        ),
    ]