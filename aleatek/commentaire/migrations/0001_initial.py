# Generated by Django 4.2 on 2023-05-31 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.CharField(max_length=200)),
                ('a_suivre', models.BooleanField(default=True)),
            ],
        ),
    ]
