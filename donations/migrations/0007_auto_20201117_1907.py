# Generated by Django 3.1.1 on 2020-11-18 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneydonation',
            name='money_total',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
    ]