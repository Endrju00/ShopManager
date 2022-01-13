from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from products.models import DeliveredItems
from clients.models import Client
from employees.models import Employee
# Create your models here.


class Address(models.Model):
    city = models.CharField(max_length=100, help_text="Please pass the name of the city.", db_column="miasto")
    street = models.CharField(max_length=100, help_text="Please pass the name of the street.", db_column="ulica")
    number = models.PositiveIntegerField(help_text="Please pass the number of a house.", db_column="nr_ulicy")
    post_code = models.CharField(max_length=6, help_text="Please pass the postal code.", db_column="kod_pocztowy")
    country = models.CharField(max_length=100, help_text="Please pass the name of the copuntry.", db_column="kraj")

    def __str__(self):
        return f'{self.country} {self.city} {self.street} {self.number}'

    class Meta:
        verbose_name_plural = "addresses"
        ordering = ['country', 'city', 'street', 'number']
        unique_together = (('city', 'street', 'number', 'post_code', 'country'),)
        db_table = 'Adresy'


class Order(models.Model):
    id = models.AutoField(primary_key=True, db_column="numer")
    date = models.DateField(default=timezone.now, help_text="Please pass the date in YYYY-MM-DD format.", db_column="data_zlozenia")
    status = models.CharField(max_length=100, help_text="Please pass the status of the order.", db_column="status")
    comment = models.TextField(max_length=1000, blank=True, null=True, help_text="Optional: Please add some comments.", db_column="komentarz")

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, help_text="Please choose the address.", db_column="id_adresu")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text="Please select the client. If client do not exist define the client in Clients section.", db_column="id_klienta")
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, help_text="Please select the employee responsible for the order.", db_column="id_pracownika")

    def __str__(self):
        return f'#{self.id} Status: {self.status}'

    class Meta:
        ordering = ['-id']
        db_table = 'Zamowienia'


class ItemInOrder(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Please define quantity of product.", db_column="ilosc_zamawiana")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column="numer_zamowienia")
    delivery = models.ForeignKey(
        DeliveredItems, on_delete=models.SET_NULL, null=True, help_text="Please select the delivery of the product.", db_column="id_dostawy")

    def __str__(self):
        return f'{self.quantity}x {self.delivery.product} for {self.delivery.unit_selling_price} PLN'

    class Meta:
        ordering = ['quantity']
        unique_together = (('delivery', 'order'),)
        db_table = 'Pozycje_w_zamowieniach'


class Payment(models.Model):
    date = models.DateTimeField(default=timezone.now, help_text="Please pass the date of the payment.", db_column="data")
    amount = models.FloatField(validators=[MinValueValidator(0)],  help_text="Please pass the amount of the payment.", db_column="kwota")

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,  help_text="Please select the order for which the payment was made.", db_column="numer_zamowienia")

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
        db_table = 'Platnosci'
