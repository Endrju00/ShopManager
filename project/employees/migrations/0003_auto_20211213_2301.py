# Generated by Django 3.2.10 on 2021-12-13 22:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_salary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['position', 'name', 'surname']},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, help_text='Optional: Please pass the email of the employee.', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='hours_per_week',
            field=models.PositiveIntegerField(help_text='Please pass the number of hours per week of the employee.'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(help_text='Please pass the name of the employee.', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(help_text='Please pass the phone number of the employee.', max_length=9),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(help_text='Please choose the position for the employee', null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.position'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.FloatField(help_text='Please pass the salary of the employee.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='employee',
            name='surname',
            field=models.CharField(help_text='Please pass the surname of the employee.', max_length=100),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(help_text='Please pass the name of the position.', max_length=100),
        ),
        migrations.AlterField(
            model_name='position',
            name='salary_max',
            field=models.FloatField(help_text='Please pass the maximum wage on this position.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='position',
            name='salary_min',
            field=models.FloatField(help_text='Please pass the minimum wage on this position.', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]