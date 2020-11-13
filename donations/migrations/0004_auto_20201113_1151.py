# Generated by Django 3.1.1 on 2020-11-13 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20201105_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timesplit',
            name='time_donation',
        ),
        migrations.AddField(
            model_name='moneydonation',
            name='charity',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='timedonation',
            name='task',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.DeleteModel(
            name='MoneySplit',
        ),
        migrations.DeleteModel(
            name='TimeSplit',
        ),
    ]
