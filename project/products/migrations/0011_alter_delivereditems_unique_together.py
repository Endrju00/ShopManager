# Generated by Django 3.2.10 on 2021-12-14 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20211214_2329'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='delivereditems',
            unique_together={('date', 'wholesaler', 'product')},
        ),
    ]