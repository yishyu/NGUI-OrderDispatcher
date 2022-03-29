# Generated by Django 4.0.3 on 2022-03-29 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_display', '0002_order_address_order_arrival_time_order_order_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_state',
            field=models.CharField(choices=[('a', 'In Queue'), ('b', 'Preparing'), ('c', 'Done')], default='a', max_length=50, verbose_name='state'),
        ),
    ]