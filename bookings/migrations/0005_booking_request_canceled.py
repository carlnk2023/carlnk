# Generated by Django 4.0.2 on 2023-02-04 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_booking_canceled_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='request_canceled',
            field=models.BooleanField(default=False),
        ),
    ]
