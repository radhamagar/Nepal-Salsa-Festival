# Generated by Django 5.0.2 on 2024-04-16 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salsa_Festival', '0012_volunteer_id_alter_volunteer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]