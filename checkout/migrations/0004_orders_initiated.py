# Generated by Django 3.0.7 on 2020-12-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20201205_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='initiated',
            field=models.BooleanField(default=False),
        ),
    ]