# Generated by Django 3.0.8 on 2021-11-01 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20211102_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffuser',
            name='work',
        ),
    ]
