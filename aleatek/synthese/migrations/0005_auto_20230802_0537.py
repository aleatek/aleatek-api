# Generated by Django 3.2.12 on 2023-08-02 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthese', '0004_synthesecomentairerv_synthesecommentairearticle_synthesecommentairedocument'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='synthesecomentairerv',
            constraint=models.UniqueConstraint(fields=('synthese', 'commentaire'), name='unique_synthese_commentaire_rv'),
        ),
        migrations.AddConstraint(
            model_name='synthesecommentairearticle',
            constraint=models.UniqueConstraint(fields=('synthese', 'commentaire'), name='unique_synthese_commentaire_article'),
        ),
        migrations.AddConstraint(
            model_name='synthesecommentairedocument',
            constraint=models.UniqueConstraint(fields=('synthese', 'commentaire'), name='unique_synthese_commentaire_document'),
        ),
    ]
