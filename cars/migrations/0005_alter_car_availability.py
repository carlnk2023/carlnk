# Generated by Django 4.0.2 on 2023-02-03 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_car_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='availability',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='YES', max_length=3),
        ),
    ]
