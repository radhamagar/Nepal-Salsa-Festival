# Generated by Django 5.0.2 on 2024-03-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_siteuser_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='siteuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='ph_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
    ]
