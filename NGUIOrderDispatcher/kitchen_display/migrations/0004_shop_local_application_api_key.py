# Generated by Django 4.0.3 on 2022-03-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_display', '0003_order_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='local_application_api_key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
