# Generated by Django 5.0.6 on 2024-07-21 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_address_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='shop.shoppingcart', verbose_name='Products'),
        ),
    ]