# Generated by Django 2.2.16 on 2022-08-16 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_auto_20220816_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(verbose_name='Год'),
        ),
    ]
