# Generated by Django 3.0.7 on 2020-06-25 21:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('sent_date', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('address1', models.CharField(blank=True, max_length=50)),
                ('address2', models.CharField(blank=True, max_length=50)),
                ('postcode', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('telephone', models.CharField(blank=True, max_length=25)),
                ('shipping', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='order_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.orders')),
            ],
        ),
    ]
