# Generated by Django 3.0.8 on 2021-11-01 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20211030_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='availabledestination',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='City/Town'),
        ),
    ]
