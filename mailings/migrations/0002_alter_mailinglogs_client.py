# Generated by Django 4.2.4 on 2023-08-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglogs',
            name='client',
            field=models.ManyToManyField(blank=True, to='mailings.client', verbose_name='Клиент'),
        ),
    ]
