# Generated by Django 4.2.4 on 2023-09-03 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0002_rename_card_cards'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
            ],
        ),
    ]
