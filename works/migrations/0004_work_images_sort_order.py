# Generated by Django 3.0.5 on 2020-05-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0003_auto_20200505_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_images',
            name='sort_order',
            field=models.SmallIntegerField(default=999),
        ),
    ]
