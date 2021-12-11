from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    email = models.EmailField(blank=True, null=True)
    discount_card_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'