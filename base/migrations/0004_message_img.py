# Generated by Django 4.1.7 on 2023-05-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='message/'),
        ),
    ]
