# Generated by Django 5.0.2 on 2024-03-18 16:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0002_alter_festival_past_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billuser',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='billuser',
            name='user',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.CharField(default='', max_length=255)),
                ('tickets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='festivals.ticket')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Bill',
        ),
        migrations.DeleteModel(
            name='BillUser',
        ),
    ]
