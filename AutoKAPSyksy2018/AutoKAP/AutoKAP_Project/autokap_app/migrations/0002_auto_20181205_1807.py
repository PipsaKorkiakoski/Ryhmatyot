# Generated by Django 2.1.3 on 2018-12-05 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autokap_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serialread',
            name='latitude',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serialread',
            name='longitude',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serialread',
            name='speed',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
