# Generated by Django 2.2.16 on 2022-08-12 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_category_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='genre', through='reviews.GenreTitle', to='reviews.Genre'),
        ),
    ]