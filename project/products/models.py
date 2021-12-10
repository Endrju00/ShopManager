from django.db import models


# Create your models here.
class Wholesaler(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    overcategory = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
    

class Product(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    producer = models.ForeignKey(Producer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class DeliveredItems(models.Model):
    date = models.DateField(auto_now=False)
    quantity = models.PositiveIntegerField()
    unit_purchase_price = models.FloatField()
    unit_selling_price = models.FloatField()

    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        self.unit_purchase_price = round(self.unit_purchase_price, 2)
        self.unit_selling_price = round(self.unit_selling_price, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product} from {self.wholesaler} {self.date}'

    class Meta:
        verbose_name_plural = "delivered items"