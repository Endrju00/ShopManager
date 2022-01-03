# Generated by Django 3.2.10 on 2021-12-14 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_delivereditems_unique_together'),
        ('orders', '0012_alter_address_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='iteminorder',
            unique_together={('delivery', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('date', 'order')},
        ),
    ]