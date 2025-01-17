# Generated by Django 4.0.7 on 2023-01-23 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0064_remove_projectrole_whitelist'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('metric_type', models.CharField(choices=[('DOCUMENTATION', 'Documentation'), ('LINTING', 'Liting'), ('DEVELOPERS', 'Developers')], max_length=25)),
                ('file_path', models.FilePathField(max_length=256)),
                ('branch', models.TextField()),
                ('result_string', models.TextField(blank=True)),
                ('result_json', models.JSONField(blank=True, default=dict)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.project')),
            ],
        ),
    ]
