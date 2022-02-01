# Generated by Django 3.2.10 on 2022-01-30 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='overcategory',
            field=models.ForeignKey(blank=True, db_column='nadkategoria', help_text='Optional: Please select an overcategory.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category'),
        ),
    ]
