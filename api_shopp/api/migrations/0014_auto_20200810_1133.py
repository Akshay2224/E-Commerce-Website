# Generated by Django 3.0.8 on 2020-08-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200810_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller_name',
            field=models.CharField(max_length=100),
        ),
    ]
