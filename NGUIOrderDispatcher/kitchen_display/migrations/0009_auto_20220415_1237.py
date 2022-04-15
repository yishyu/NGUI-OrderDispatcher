# Generated by Django 3.2.12 on 2022-04-15 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen_display', '0008_alter_dish_identifier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='color')),
                ('hex_or_rgba', models.CharField(max_length=50, verbose_name='color code')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen_display.color', verbose_name='color'),
        ),
    ]
