# Generated by Django 2.2.16 on 2022-08-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20220809_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('administrator', 'Администратор'), ('moderator', 'Модератор'), ('user', 'Пользователь')], default='user', max_length=30, verbose_name='Роль'),
        ),
    ]
