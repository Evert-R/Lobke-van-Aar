# Generated by Django 3.0.5 on 2020-04-21 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
        ('works', '0010_auto_20200420_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_items',
            name='shop_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.shop_items'),
        ),
    ]