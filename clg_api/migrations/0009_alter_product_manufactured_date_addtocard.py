# Generated by Django 4.0 on 2022-09-22 13:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_order_location'),
        ('clg_api', '0008_alter_product_manufactured_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='manufactured_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 22, 19, 6, 50, 795355), null=True),
        ),
        migrations.CreateModel(
            name='AddToCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='user.user')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='clg_api.product')),
            ],
        ),
    ]