# Generated by Django 4.1 on 2022-08-21 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_skill_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='user-default.jpg', null=True, upload_to='user-images/'),
        ),
    ]
