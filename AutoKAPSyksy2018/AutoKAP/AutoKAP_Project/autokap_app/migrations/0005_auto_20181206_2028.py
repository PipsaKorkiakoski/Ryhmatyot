# Generated by Django 2.1.3 on 2018-12-06 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autokap_app', '0004_auto_20181206_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serialread',
            name='buf',
        ),
        migrations.RemoveField(
            model_name='serialread',
            name='direction',
        ),
        migrations.RemoveField(
            model_name='serialread',
            name='line',
        ),
        migrations.RemoveField(
            model_name='serialread',
            name='status',
        ),
    ]