# Generated by Django 2.2.16 on 2022-08-08 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220808_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(blank=True, max_length=15, null=True, verbose_name='Пароль'),
        ),
    ]
