# Generated by Django 5.0.2 on 2024-03-18 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0010_remove_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='max_amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
