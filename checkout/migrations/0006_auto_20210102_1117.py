# Generated by Django 3.0.7 on 2021-01-02 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_auto_20201211_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='initiated',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='order_number',
        ),
        migrations.AddField(
            model_name='orders',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
    ]
