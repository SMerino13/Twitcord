# Generated by Django 4.1.7 on 2023-05-23 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_friend_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='RePosted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.userprofile')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
