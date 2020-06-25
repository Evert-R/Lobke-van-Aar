# Generated by Django 3.0.7 on 2020-06-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='materials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_text', models.CharField(blank=True, max_length=3000)),
            ],
        ),
        migrations.CreateModel(
            name='shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='shop_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('on_sale', models.BooleanField(default=False)),
                ('discount', models.SmallIntegerField(default=0)),
                ('stock', models.SmallIntegerField(default=0)),
                ('edition_count', models.SmallIntegerField(default=0)),
                ('frame', models.CharField(blank=True, choices=[('FR', 'Frame'), ('NF', 'No Frame')], max_length=2, null=True)),
                ('signed', models.BooleanField(default=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('personal_message', models.CharField(blank=True, max_length=2000)),
                ('personal_text', models.BooleanField(default=False)),
                ('standard_text', models.BooleanField(default=True)),
                ('sort_order', models.SmallIntegerField(default=999)),
            ],
        ),
        migrations.CreateModel(
            name='shop_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(blank=True, max_length=200)),
                ('show', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='work_sizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='work_types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
