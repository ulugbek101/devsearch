# Generated by Django 4.1.1 on 2022-09-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_remove_message_full_name_message_fullname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='fullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
