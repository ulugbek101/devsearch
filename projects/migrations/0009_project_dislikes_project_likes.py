# Generated by Django 4.1.1 on 2022-09-30 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
