# Generated by Django 5.1.1 on 2024-09-18 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_service', '0002_alter_order_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='orders',
        ),
    ]
