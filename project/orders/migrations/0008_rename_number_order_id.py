# Generated by Django 3.2.10 on 2021-12-11 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='number',
            new_name='id',
        ),
    ]