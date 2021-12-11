from django.db import models

from products.models import DeliveredItems


# Create your models here.
class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    post_code = models.CharField(max_length=6)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.street} {self.number} {self.city} {self.country}'


class Order(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    date = models.DateField()
    status = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)

    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    # client
    # employee

    def __str__(self):
        return f'#{self.number} Status: {self.status}'


class ItemInOrder(models.Model):
    quantity = models.PositiveIntegerField()
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery = models.ForeignKey(DeliveredItems, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.delivery.product} in #{self.order.number}'


class Payment(models.Model):
    date = models.DateTimeField()
    amount = models.FloatField()

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Payment ({self.amount}$) for #{self.order.number}'
    