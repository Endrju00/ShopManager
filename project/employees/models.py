from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the position.")
    salary_min = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the minimum wage on this position.")
    salary_max = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the maximum wage on this position.")

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


class Employee(models.Model):
    name = models.CharField(max_length=100, help_text="Please pass the name of the employee.")
    surname = models.CharField(max_length=100, help_text="Please pass the surname of the employee.")
    phone_number = models.CharField(max_length=9, help_text="Please pass the phone number of the employee.")
    email = models.EmailField(blank=True, null=True, help_text="Optional: Please pass the email of the employee.")
    salary = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the salary of the employee.")
    hours_per_week = models.PositiveIntegerField(help_text="Please pass the number of hours per week of the employee.")
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, help_text="Please choose the position for the employee")

    def save(self, *args, **kwargs):
        self.salary = min(max(round(self.salary, 2), self.position.salary_min),
                          self.position.salary_max)  # assure salary_min < salary < salary_max
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.position} {self.name} {self.surname}'

    class Meta:
        ordering = ['position', 'name', 'surname']
