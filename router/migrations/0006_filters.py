# Generated by Django 4.2.4 on 2023-09-07 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('router', '0005_cardimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_choice', models.BooleanField()),
                ('title', models.CharField(max_length=100)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='router.categories')),
            ],
        ),
    ]