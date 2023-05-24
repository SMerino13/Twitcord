# Generated by Django 4.1.7 on 2023-05-22 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_post_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='base.userprofile'),
            preserve_default=False,
        ),
    ]