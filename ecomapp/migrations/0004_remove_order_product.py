# Generated by Django 2.2.14 on 2021-05-05 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
