# Generated by Django 5.0.2 on 2024-04-19 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0018_alter_festival_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='lobby_id',
            field=models.IntegerField(default=0),
        ),
    ]