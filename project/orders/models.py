from django.db import models
from django.core.validators import MinValueValidator

from products.models import DeliveredItems
from clients.models import Client
from employees.models import Employee

# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=100, help_text="Please pass the name of the city.")
    street = models.CharField(max_length=100, help_text="Please pass the name of the street.")
    number = models.PositiveIntegerField(help_text="Please pass the number of a house.")
    post_code = models.CharField(max_length=6, help_text="Please pass the postal code.")
    country = models.CharField(max_length=100, help_text="Please pass the name of the copuntry.")

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.number}'

    class Meta:
        verbose_name_plural = "addresses"
        ordering = ['country', 'city', 'street', 'number']
        unique_together = (('city', 'street', 'number', 'post_code', 'country'),)


class Order(models.Model):
    date = models.DateField(help_text="Please pass the date in YYYY-MM-DD format.")
    status = models.CharField(max_length=100, help_text="Please pass the status of the order.")
    comment = models.TextField(max_length=1000, blank=True, null=True, help_text="Optional: Please add some comments.")

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, help_text="Please choose the address.")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text="Please select the client. If client do not exist define the client in Clients section.")
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, help_text="Please select the employee responsible for the order.")

    def __str__(self):
        return f'#{self.id} Status: {self.status}'

    class Meta:
        ordering = ['-id']


class ItemInOrder(models.Model):
    quantity = models.PositiveIntegerField(help_text="Please define quantity of product.")

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery = models.ForeignKey(
        DeliveredItems, on_delete=models.SET_NULL, null=True, help_text="Please select the delivery of the product.")

    def __str__(self):
        return f'{self.quantity}x {self.delivery.product} for {self.delivery.unit_selling_price} PLN'

    class Meta:
        ordering = ['quantity']
        unique_together = (('delivery', 'order'),)


class Payment(models.Model):
    date = models.DateTimeField(help_text="Please pass the date of the payment.")
    amount = models.FloatField(validators=[MinValueValidator(0)],  help_text="Please pass the amount of the payment.")

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,  help_text="Please select the order for which the payment was made.")

    def __str__(self):
        if self.order:
            return f'Payment #{self.id} for order #{self.order.id}'
        return f'Payment #{self.id}'

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        unique_together = (('date', 'order'),)
