# Generated by Django 4.1.7 on 2023-05-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='static/img/discord-icon.svg', null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='banner',
            field=models.ImageField(blank=True, default='static/img/header.jpg', null=True, upload_to='banners/'),
        ),
    ]