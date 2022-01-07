# Generated by Django 3.2.10 on 2022-01-07 15:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='imie', help_text="Please pass the client's name.", max_length=100)),
                ('surname', models.CharField(db_column='nazwisko', help_text="Please pass the client's surname.", max_length=100)),
                ('phone_number', models.CharField(db_column='nr_telefonu', help_text="Please pass the client's phone number.", max_length=9, validators=[django.core.validators.MinLengthValidator(9)])),
                ('email', models.EmailField(blank=True, db_column='email', help_text="Optional: Please pass the client's email.", max_length=254, null=True)),
                ('discount_card_code', models.CharField(blank=True, db_column='kod_karty_rabatowej', help_text="Optional: Please pass the client's discount card code.", max_length=100, null=True)),
            ],
            options={
                'db_table': 'Klienci',
                'ordering': ['name', 'surname', 'phone_number'],
            },
        ),
    ]
