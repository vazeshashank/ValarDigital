# Generated by Django 4.2.7 on 2023-11-23 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0003_products_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
