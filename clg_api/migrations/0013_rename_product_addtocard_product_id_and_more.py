# Generated by Django 4.0 on 2022-09-22 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clg_api', '0012_alter_product_manufactured_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addtocard',
            old_name='product',
            new_name='product_id',
        ),
        migrations.AlterField(
            model_name='product',
            name='manufactured_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 22, 20, 38, 21, 65917), null=True),
        ),
    ]