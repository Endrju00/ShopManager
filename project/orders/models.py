from django.db import models
from django.core.validators import MinValueValidator

from products.models import DeliveredItems
from clients.models import Client
from employees.models import Employee

# Create your models here.
class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    post_code = models.CharField(max_length=6)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} {self.number} {self.city} {self.country}'

    class Meta:
        verbose_name_plural = "addresses"


class Order(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'#{self.id} Status: {self.status}'


class ItemInOrder(models.Model):
    quantity = models.PositiveIntegerField()
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery = models.ForeignKey(DeliveredItems, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.delivery.product} in #{self.order.id}'
    

class Payment(models.Model):
    date = models.DateTimeField()
    amount = models.FloatField(validators=[MinValueValidator(0)])

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Payment for order #{self.order.id}'
    
    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super().save(*args, **kwargs)
    