# Generated by Django 3.2.19 on 2023-06-18 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvrage', '0023_alter_aso_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='codification',
            field=models.CharField(choices=[('F', 'F'), ('RMQ', 'RMQ'), ('HM', 'HM'), ('VI', 'VI')], max_length=23),
        ),
    ]
