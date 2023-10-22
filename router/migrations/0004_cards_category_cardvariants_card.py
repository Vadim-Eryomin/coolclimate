# Generated by Django 4.2.4 on 2023-09-04 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0003_cardvariants_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='router.categories'),
        ),
        migrations.AddField(
            model_name='cardvariants',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='router.cards'),
        ),
    ]
