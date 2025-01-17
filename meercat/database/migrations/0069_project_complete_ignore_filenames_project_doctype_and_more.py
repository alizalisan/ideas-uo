# Generated by Django 4.0.7 on 2023-01-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0068_project_complete_ignore_extensions'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='complete_ignore_filenames',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='project',
            name='doctype',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='project',
            name='documentation_ignore_extensions',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='project',
            name='documentation_ignore_filenames',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='project',
            name='language',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
