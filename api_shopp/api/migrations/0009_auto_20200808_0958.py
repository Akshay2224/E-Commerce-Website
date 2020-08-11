# Generated by Django 3.0.8 on 2020-08-08 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_account_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selleraccount',
            name='user',
        ),
        migrations.AlterField(
            model_name='selleraccount',
            name='company_name',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='selleraccount',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserProfileInfo',
        ),
    ]
