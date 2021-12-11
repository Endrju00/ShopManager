from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100)
    salary_min = models.FloatField(validators=[MinValueValidator(0)])
    salary_max = models.FloatField(validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        min_salary, max_salary = self.salary_min, self.salary_max
        self.salary_min = round(min(min_salary, max_salary), 2) # assure min < max
        self.salary_max = round(max(min_salary, max_salary), 2) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=9)
    email = models.EmailField(blank=True, null=True)
    salary = models.FloatField(validators=[MinValueValidator(0)])
    hours_per_week = models.PositiveIntegerField()
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.salary = min(max(round(self.salary, 2), self.position.salary_min), self.position.salary_max)  # assure salary_min < salary < salary_max
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.position} {self.name} {self.surname}'
         