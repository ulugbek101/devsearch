# Generated by Django 4.1 on 2022-08-21 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='user-default.png', null=True, upload_to='user-images/'),
        ),
    ]