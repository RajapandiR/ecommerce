# Generated by Django 2.2.14 on 2021-04-07 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('admin', '0004_auto_20210407_1336'),
        ('ecomapp', '0007_auto_20210407_1234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='User1',
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='id'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='id'),
        ),
    ]
