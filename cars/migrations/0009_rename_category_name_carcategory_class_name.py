# Generated by Django 4.0.2 on 2023-02-09 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_delete_car_carcategory_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carcategory',
            old_name='category_name',
            new_name='class_name',
        ),
    ]
