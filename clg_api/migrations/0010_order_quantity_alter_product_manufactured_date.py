# Generated by Django 4.0 on 2022-09-22 13:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_api', '0009_alter_product_manufactured_date_addtocard'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufactured_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 22, 19, 7, 43, 297024), null=True),
        ),
    ]
