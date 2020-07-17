# Generated by Django 3.0.7 on 2020-07-17 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medbot_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='med_ids',
            field=models.ManyToManyField(to='medbot_app.Inventory'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_quantity',
            field=models.IntegerField(default=5),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('adding_quantity', models.IntegerField(default=5)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medbot_app.Customer')),
                ('med_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medbot_app.Inventory')),
                ('pharmacy_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medbot_app.Employee')),
            ],
        ),
    ]