# Generated by Django 3.0.8 on 2021-11-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0010_auto_20211103_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courier',
            name='pickup_date',
            field=models.DateField(blank=True, null=True, verbose_name='Pick Up Date'),
        ),
    ]
