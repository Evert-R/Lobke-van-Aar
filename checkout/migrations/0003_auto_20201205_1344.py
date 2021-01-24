# Generated by Django 3.0.7 on 2020-12-05 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_items_work_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_number',
            field=models.CharField(default=1, editable=False, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order_items',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='checkout.orders'),
        ),
    ]
