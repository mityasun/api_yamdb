# Generated by Django 2.2.16 on 2022-08-16 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20220816_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(max_length=4, verbose_name='Год'),
        ),
    ]
