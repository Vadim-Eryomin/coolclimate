# Generated by Django 4.2.4 on 2023-09-16 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0008_alter_filters_is_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='cards',
            name='description',
            field=models.CharField(max_length=6000, null=True),
        ),
    ]
