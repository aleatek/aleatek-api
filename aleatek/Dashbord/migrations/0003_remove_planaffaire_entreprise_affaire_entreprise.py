# Generated by Django 4.2 on 2023-06-01 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0004_rename_responsable_responsable_entreprise'),
        ('Dashbord', '0002_alter_affaire_statut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planaffaire',
            name='entreprise',
        ),
        migrations.AddField(
            model_name='affaire',
            name='entreprise',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='entreprise.entreprise'),
            preserve_default=False,
        ),
    ]
