# Generated by Django 5.0.2 on 2024-03-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0003_remove_billuser_bill_remove_billuser_user_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
