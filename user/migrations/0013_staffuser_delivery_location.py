# Generated by Django 3.0.8 on 2021-11-01 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_remove_availabledestination_delivery_boys'),
        ('user', '0012_remove_staffuser_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffuser',
            name='delivery_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='general.AvailableDestination', verbose_name='Delivery Location'),
        ),
    ]
