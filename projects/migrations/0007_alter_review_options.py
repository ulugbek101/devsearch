# Generated by Django 4.1 on 2022-09-04 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_review_options_remove_project_vote_ratio_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('created',)},
        ),
    ]