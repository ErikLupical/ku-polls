# Generated by Django 5.1 on 2024-09-17 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
    ]
