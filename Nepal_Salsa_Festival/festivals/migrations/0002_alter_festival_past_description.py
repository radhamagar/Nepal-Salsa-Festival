# Generated by Django 5.0.2 on 2024-03-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festival',
            name='past_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
