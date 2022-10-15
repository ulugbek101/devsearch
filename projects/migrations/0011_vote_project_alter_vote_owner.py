# Generated by Django 4.1.1 on 2022-09-30 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_profile_image'),
        ('projects', '0010_remove_project_dislikes_remove_project_likes_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
