# Generated by Django 3.2.10 on 2022-01-07 15:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(db_column='nazwa', help_text='Please pass the name of the category.', max_length=100, primary_key=True, serialize=False)),
                ('overcategory', models.ForeignKey(blank=True, db_column='nadkategoria', help_text='Optional: Please select an overcategory.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'db_table': 'Kategorie',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('name', models.CharField(db_column='nazwa', help_text='Please pass the name of the producer.', max_length=100, primary_key=True, serialize=False)),
                ('website', models.CharField(db_column='strona_www', help_text='Please pass the website of the producer.', max_length=100)),
            ],
            options={
                'db_table': 'Producenci',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Wholesaler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='nazwa', help_text='Please pass the name of the wholesaler.', max_length=100)),
            ],
            options={
                'db_table': 'Hurtownie',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.PositiveBigIntegerField(db_column='kod', help_text='Please pass the code of the product.', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='nazwa', help_text='Please pass the name of the product.', max_length=100)),
                ('description', models.TextField(blank=True, db_column='opis', help_text='Optional: Please pass the description of the product.', max_length=1000)),
                ('category', models.ForeignKey(db_column='kategoria', help_text='Please select the category of the product.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
                ('producer', models.ForeignKey(db_column='producent', help_text='Please select the producer of the producer.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.producer')),
            ],
            options={
                'db_table': 'Produkty',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DeliveredItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_column='data', help_text='Please pass the date of the delivery in YYYY-MM-DD format.')),
                ('quantity', models.PositiveIntegerField(db_column='ilosc', help_text='Please pass the quantity of the delivered items.')),
                ('unit_purchase_price', models.FloatField(db_column='cena_jednostkowa_zakupu', help_text='Please pass the unit purchase price of the delivered items.', validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_selling_price', models.FloatField(db_column='cena_jednostkowa_sprzedazy', help_text='Please pass the unit selling price of the delivered items.', validators=[django.core.validators.MinValueValidator(0)])),
                ('product', models.ForeignKey(db_column='kod_produktu', help_text='Please select the product that has been delivered.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('wholesaler', models.ForeignKey(db_column='id_hurtownii', help_text='Please select the wholesaler of the delivered items.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.wholesaler')),
            ],
            options={
                'verbose_name_plural': 'delivered items',
                'db_table': 'Dostarczone_towary',
                'ordering': ['-date'],
                'unique_together': {('date', 'wholesaler', 'product')},
            },
        ),
    ]
