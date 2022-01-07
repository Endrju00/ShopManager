# Generated by Django 3.2.10 on 2022-01-07 14:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('name', models.CharField(db_column='nazwa', help_text='Please pass the name of the position.', max_length=100, primary_key=True, serialize=False)),
                ('salary_min', models.FloatField(db_column='placa_min', help_text='Please pass the minimum wage on this position.', validators=[django.core.validators.MinValueValidator(0)])),
                ('salary_max', models.FloatField(db_column='placa_max', help_text='Please pass the maximum wage on this position.', validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'db_table': 'Stanowiska',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='imie', help_text='Please pass the name of the employee.', max_length=100)),
                ('surname', models.CharField(db_column='nazwisko', help_text='Please pass the surname of the employee.', max_length=100)),
                ('phone_number', models.CharField(db_column='nr_telefonu', help_text='Please pass the phone number of the employee.', max_length=9, validators=[django.core.validators.MinLengthValidator(9)])),
                ('email', models.EmailField(blank=True, db_column='email', help_text='Optional: Please pass the email of the employee.', max_length=254, null=True)),
                ('salary', models.FloatField(db_column='placa', help_text='Please pass the salary of the employee.', validators=[django.core.validators.MinValueValidator(0)])),
                ('hours_per_week', models.PositiveIntegerField(db_column='ilosc_godzin_tyg', help_text='Please pass the number of hours per week of the employee.', validators=[django.core.validators.MaxValueValidator(168)])),
                ('position', models.ForeignKey(db_column='nazwa_stanowiska', help_text='Please choose the position for the employee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.position')),
            ],
            options={
                'db_table': 'Pracownicy',
                'ordering': ['position', 'name', 'surname'],
            },
        ),
    ]
