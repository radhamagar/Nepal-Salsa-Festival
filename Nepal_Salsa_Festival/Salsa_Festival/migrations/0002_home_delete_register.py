# Generated by Django 5.0 on 2024-02-04 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salsa_Festival', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_img', models.ImageField(upload_to='images/')),
                ('home_description', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Register',
        ),
    ]