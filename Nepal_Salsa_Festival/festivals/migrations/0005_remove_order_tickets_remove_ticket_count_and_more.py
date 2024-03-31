# Generated by Django 5.0.2 on 2024-03-18 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0004_ticket_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tickets',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='count',
        ),
        migrations.CreateModel(
            name='TicketAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='festivals.ticket')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='festivals.ticketamount'),
            preserve_default=False,
        ),
    ]
