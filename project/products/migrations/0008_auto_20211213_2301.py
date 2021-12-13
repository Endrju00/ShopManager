# Generated by Django 3.2.10 on 2021-12-13 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='delivereditems',
            options={'ordering': ['-date'], 'verbose_name_plural': 'delivered items'},
        ),
        migrations.AlterModelOptions(
            name='producer',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='wholesaler',
            options={'ordering': ['name']},
        ),
    ]
