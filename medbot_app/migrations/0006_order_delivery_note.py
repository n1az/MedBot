# Generated by Django 3.0.7 on 2020-07-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medbot_app', '0005_order_order_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_note',
            field=models.CharField(default='Call me when you arrive', max_length=100),
        ),
    ]
