# Generated by Django 4.1.7 on 2023-05-23 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_friend_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together={('user1', 'user2'), ('user2', 'user1')},
        ),
    ]
