# Generated by Django 4.0.3 on 2022-03-31 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_display', '0007_dish_identifier_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='identifier',
            field=models.CharField(default='', max_length=10, verbose_name='remote identifier'),
        ),
    ]
