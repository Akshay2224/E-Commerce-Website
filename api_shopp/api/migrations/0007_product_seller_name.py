# Generated by Django 3.0.8 on 2020-08-06 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_product_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seller_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
