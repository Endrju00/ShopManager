from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

import orders.models

# Create your models here.
class Wholesaler(models.Model):
    name = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the wholesaler.", db_column="nazwa")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        db_table = 'Hurtownie'


class Producer(models.Model):
    name = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the producer.", db_column="nazwa")
    website = models.CharField(max_length=100, help_text="Please pass the website of the producer.", db_column="strona_www")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        db_table = 'Producenci'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the category.", db_column="nazwa")

    overcategory = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True, help_text="Optional: Please select an overcategory.", db_column="nadkategoria")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
        db_table = 'Kategorie'
    

class Product(models.Model):
    code = models.PositiveBigIntegerField(unique=True, help_text="Please pass the code of the product.", db_column="kod")
    name = models.CharField(max_length=100, help_text="Please pass the name of the product.", db_column="nazwa")
    description = models.TextField(max_length=1000, blank=True, help_text="Optional: Please pass the description of the product.", db_column="opis")

    category = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True, help_text="Please select the category of the product.", db_column="kategoria")
    producer = models.ForeignKey(Producer, on_delete=models.RESTRICT, null=True, help_text="Please select the producer of the producer.", db_column="producent")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'Produkty'


class DeliveredItems(models.Model):
    date = models.DateField(default=timezone.now, auto_now=False, help_text="Please pass the date of the delivery in YYYY-MM-DD format.", db_column="data")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Please pass the quantity of the delivered items.", db_column="ilosc")
    unit_purchase_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit purchase price of the delivered items.", db_column="cena_jednostkowa_zakupu")
    unit_selling_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit selling price of the delivered items.", db_column="cena_jednostkowa_sprzedazy")

    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.RESTRICT, null=True, help_text="Please select the wholesaler of the delivered items.", db_column="hurtownia")
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True, help_text="Please select the product that has been delivered.", db_column="kod_produktu")

    def save(self, *args, **kwargs):
        self.unit_purchase_price = round(self.unit_purchase_price, 2)
        self.unit_selling_price = round(self.unit_selling_price, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        name = ''
        if self.product and self.wholesaler:
            name = f'{self.date} {self.product} from {self.wholesaler}'
        elif self.product and not self.wholesaler:
            name = f'{self.date} {self.product} from Unknown wholesaler'
        elif not self.product and self.wholesaler:
            name = f'{self.date} Unknown product from {self.wholesaler}'
        else:
            name = f'Unknown delivery {self.date}'
        
        available = self.quantity
        items = orders.models.ItemInOrder.objects.filter(delivery__id=self.id)
        for item in items:
            available -= item.quantity
            
        return f'{name} ({available} left)'


    class Meta:
        verbose_name_plural = "delivered items"
        ordering = ['-date']
        unique_together = (('date', 'wholesaler', 'product'),)
        db_table = 'Dostarczone_towary'
