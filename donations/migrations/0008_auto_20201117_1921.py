# Generated by Django 3.1.1 on 2020-11-18 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20201117_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charity',
            name='desc',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='charity',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='task',
            name='desc',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
