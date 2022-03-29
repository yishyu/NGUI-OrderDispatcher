# Generated by Django 4.0.3 on 2022-03-29 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kitchen_display.category', verbose_name='Categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=50, verbose_name='order id')),
                ('fetched_time', models.DateTimeField(auto_now=True, verbose_name='fetched_time')),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='', max_length=126, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('employees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderToDishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen_display.dish', verbose_name='dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen_display.order', verbose_name='order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(through='kitchen_display.OrderToDishes', to='kitchen_display.dish', verbose_name='dish'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kitchen_display.shop', verbose_name='shop'),
        ),
    ]
