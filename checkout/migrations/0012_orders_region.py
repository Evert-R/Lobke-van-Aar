# Generated by Django 3.0.7 on 2021-03-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_orders_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='region',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
