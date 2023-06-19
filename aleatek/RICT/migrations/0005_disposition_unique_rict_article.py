# Generated by Django 3.2.19 on 2023-06-19 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RICT', '0004_remove_disposition_type'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='disposition',
            constraint=models.UniqueConstraint(fields=('rict', 'article'), name='unique_rict_article'),
        ),
    ]
