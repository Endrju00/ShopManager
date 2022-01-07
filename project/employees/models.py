from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the position.", unique=True, db_column="nazwa")
    salary_min = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the minimum wage on this position.", db_column="placa_min")
    salary_max = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the maximum wage on this position.", db_column="placa_max")

    def save(self, *args, **kwargs):
        min_salary, max_salary = self.salary_min, self.salary_max
        self.salary_min = round(
            min(min_salary, max_salary), 2)  # assure min < max
        self.salary_max = round(max(min_salary, max_salary), 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'Stanowiska'


class Employee(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the employee.", db_column="imie")
    surname = models.CharField(max_length=100, help_text="Please pass the surname of the employee.", db_column="nazwisko")
    phone_number = models.CharField(validators=[MinLengthValidator(9)], max_length=9, help_text="Please pass the phone number of the employee.", db_column="nr_telefonu")
    email = models.EmailField(blank=True, null=True, help_text="Optional: Please pass the email of the employee.", db_column="email")
    salary = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the salary of the employee.", db_column="placa")
    hours_per_week = models.PositiveIntegerField(validators=[MaxValueValidator(168)], help_text="Please pass the number of hours per week of the employee.", db_column="ilosc_godzin_tyg")
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, help_text="Please choose the position for the employee", db_column="id_stanowiska")

    def save(self, *args, **kwargs):
        self.salary = min(max(round(self.salary, 2), self.position.salary_min),
                          self.position.salary_max)  # assure salary_min < salary < salary_max
        super().save(*args, **kwargs)

    def __str__(self):
        if self.position:
            return f'{self.position} {self.name} {self.surname}'
        return f'Unknown position {self.name} {self.surname}'

    class Meta:
        ordering = ['position', 'name', 'surname']
        db_table = 'Pracownicy'
