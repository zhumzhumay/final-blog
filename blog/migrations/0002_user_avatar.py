# Generated by Django 4.1 on 2023-06-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='ava-default.png', upload_to='', verbose_name='Аватарка'),
        ),
    ]
