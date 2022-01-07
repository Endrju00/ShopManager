from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the client's name.", db_column="imie")
    surname = models.CharField(max_length=100, help_text="Please pass the client's surname.", db_column="nazwisko")
    phone_number = models.CharField(validators=[MinLengthValidator(9)], max_length=9, help_text="Please pass the client's phone number.", db_column="nr_telefonu")
    email = models.EmailField(blank=True, null=True, help_text="Optional: Please pass the client's email.", db_column="email")
    discount_card_code = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Please pass the client's discount card code.", db_column="kod_karty_rabatowej")

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    class Meta:
        ordering = ['name', 'surname', 'phone_number']
        db_table = 'Klienci'
        