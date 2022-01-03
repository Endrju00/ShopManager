from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Wholesaler(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the wholesaler.", unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Producer(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the producer.", unique=True)
    website = models.CharField(max_length=100, help_text="Please pass the website of the producer.")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the category.", unique=True)

    overcategory = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, help_text="Optional: Please select an overcategory.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    

class Product(models.Model):
    code = models.PositiveBigIntegerField(primary_key=True, help_text="Please pass the code of the product.")
    name = models.CharField(max_length=100, help_text="Please pass the name of the product.")
    description = models.TextField(max_length=1000, blank=True, help_text="Optional: Please pass the description of the product.")

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text="Please select the category of the product.")
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True, help_text="Please select the producer of the producer.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class DeliveredItems(models.Model):
    date = models.DateField(auto_now=False, help_text="Please pass the date of the delivery in YYYY-MM-DD format.")
    quantity = models.PositiveIntegerField(help_text="Please pass the quantity of the delivered items.")
    unit_purchase_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit purchase price of the delivered items.")
    unit_selling_price = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit selling price of the delivered items.")

    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.SET_NULL, null=True, help_text="Please select the wholesaler of the delivered items.")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, help_text="Please select the product that has been delivered.")

    def save(self, *args, **kwargs):
        self.unit_purchase_price = round(self.unit_purchase_price, 2)
        self.unit_selling_price = round(self.unit_selling_price, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.date} {self.product} from {self.wholesaler}'

    class Meta:
        verbose_name_plural = "delivered items"
        ordering = ['-date']
        unique_together = (('date', 'wholesaler', 'product'),)
