# Generated by Django 3.0.8 on 2020-08-10 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200810_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Seller'),
        ),
    ]