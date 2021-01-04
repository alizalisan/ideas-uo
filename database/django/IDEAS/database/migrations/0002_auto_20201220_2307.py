# Generated by Django 3.0.4 on 2020-12-20 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['username', 'email'], 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='commit',
            options={'ordering': ['datetime'], 'verbose_name': 'commit', 'verbose_name_plural': 'commits'},
        ),
        migrations.AlterModelOptions(
            name='diff',
            options={'verbose_name': 'diff', 'verbose_name_plural': 'diffs'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name', 'source_url'], 'verbose_name': 'project', 'verbose_name_plural': 'projects'},
        ),
        migrations.AddField(
            model_name='diff',
            name='body',
            field=models.TextField(default='should be changed'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='author',
            table='author',
        ),
        migrations.AlterModelTable(
            name='commit',
            table='commit',
        ),
        migrations.AlterModelTable(
            name='diff',
            table='diff',
        ),
        migrations.AlterModelTable(
            name='project',
            table='project',
        ),
        migrations.AlterOrderWithRespectTo(
            name='diff',
            order_with_respect_to='commit',
        ),
    ]
