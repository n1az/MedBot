# Generated by Django 3.0.7 on 2020-09-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medbot_app', '0009_order_pharmacy_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_latiT',
            field=models.CharField(default='20.40', max_length=20),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_longT',
            field=models.CharField(default='90.40', max_length=20),
        ),
    ]
