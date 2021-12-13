from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the client's name.")
    surname = models.CharField(max_length=100, help_text="Please pass the client's surname.")
    phone_number = models.CharField(max_length=9, help_text="Please pass the client's phone number.")
    email = models.EmailField(blank=True, null=True, help_text="Optional: Please pass the client's email.")
    discount_card_code = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Please pass the client's discount card code.")

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    class Meta:
        ordering = ['name', 'surname', 'phone_number']
        