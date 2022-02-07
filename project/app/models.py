from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from .validators import validate_phone_number

class Adres(models.Model):
    miasto = models.CharField(max_length=100, help_text="Please pass the name of the city.")
    ulica = models.CharField(max_length=100, help_text="Please pass the name of the street.")
    nr_ulicy = models.PositiveIntegerField(help_text="Please pass the number of a house.")
    kod_pocztowy = models.CharField(max_length=6, help_text="Please pass the postal code.")
    kraj = models.CharField(max_length=100, help_text="Please pass the name of the country.")

    class Meta:
        managed = False
        db_table = 'adresy'
        unique_together = (('miasto', 'ulica', 'nr_ulicy', 'kod_pocztowy', 'kraj'),)
        ordering = ['kraj', 'miasto', 'ulica', 'nr_ulicy']
    
    def __str__(self):
        return f'{self.kraj} {self.miasto} {self.ulica} {self.nr_ulicy}'


class Producent(models.Model):
    nazwa = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the producer.")
    strona_www = models.CharField(max_length=100, blank=True, null=True, help_text="Please pass the website of the producer.")

    class Meta:
        managed = False
        db_table = 'producenci'
        ordering = ['nazwa']
    
    def __str__(self):
        return self.nazwa


class Hurtownia(models.Model):
    nazwa = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the wholesaler.")

    class Meta:
        managed = False
        db_table = 'hurtownie'
        ordering = ['nazwa']
    
    def __str__(self):
        return self.nazwa


class Kategoria(models.Model):
    nazwa = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the category.")
    id_nadkategorii = models.ForeignKey('self', models.DO_NOTHING, db_column='id_nadkategorii', blank=True, null=True, help_text="Optional: Please select an overcategory.")

    class Meta:
        managed = False
        db_table = 'kategorie'
        ordering = ['nazwa']

    def __str__(self):
        if self.id_nadkategorii:
            return f'{self.id_nadkategorii} -> {self.nazwa}'
        return self.nazwa


class Klient(models.Model):
    imie = models.CharField(max_length=100, help_text="Please pass the client's name.")
    nazwisko = models.CharField(max_length=100, help_text="Please pass the client's surname.")
    nr_telefonu = models.CharField(max_length=9, validators=[MinLengthValidator(9), validate_phone_number], help_text="Please pass the client's phone number.")
    email = models.EmailField(max_length=254, blank=True, null=True, help_text="Optional: Please pass the client's email.")
    kod_karty_rabatowej = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Please pass the client's discount card code.")

    class Meta:
        managed = False
        db_table = 'klienci'
        ordering = ['imie', 'nazwisko']

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'


class Stanowisko(models.Model):
    nazwa = models.CharField(unique=True, max_length=100, help_text="Please pass the name of the position.")
    placa_min = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the minimum wage on this position.")
    placa_max = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the maximum wage on this position.")

    class Meta:
        managed = False
        db_table = 'stanowiska'
        ordering = ['nazwa']

    def __str__(self):
        return f'{self.nazwa}'
    
    def save(self, *args, **kwargs):
        min_salary, max_salary = self.placa_min, self.placa_max
        self.placa_min = round(
            min(min_salary, max_salary), 2)  # assure min < max
        self.placa_max = round(max(min_salary, max_salary), 2)
        super().save(*args, **kwargs)


class Pracownik(models.Model):
    imie = models.CharField(max_length=100, help_text="Please pass the name of the employee.")
    nazwisko = models.CharField(max_length=100, help_text="Please pass the surname of the employee.")
    nr_telefonu = models.CharField(max_length=9, validators=[MinLengthValidator(9), validate_phone_number], help_text="Please pass the phone number of the employee.")
    email = models.EmailField(max_length=254, blank=True, null=True, help_text="Optional: Please pass the email of the employee.")
    placa = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the salary of the employee.")
    ilosc_godzin_tyg = models.PositiveIntegerField(validators=[MaxValueValidator(168)], help_text="Please pass the number of hours per week of the employee.")
    id_stanowiska = models.ForeignKey('Stanowisko', models.DO_NOTHING, db_column='id_stanowiska', help_text="Please choose the position for the employee")

    class Meta:
        managed = False
        db_table = 'pracownicy'
        ordering = ['imie', 'nazwisko']

    def __str__(self):
        return f'{self.imie} {self.nazwisko}'

    def save(self, *args, **kwargs):
        self.placa = min(max(round(self.placa, 2), self.id_stanowiska.placa_min),
                          self.id_stanowiska.placa_max)  # assure salary_min < salary < salary_max
        super().save(*args, **kwargs)


class Produkt(models.Model):
    kod = models.PositiveBigIntegerField(unique=True, help_text="Please pass the code of the product.")
    nazwa = models.CharField(max_length=100, help_text="Please pass the name of the product.")
    opis = models.TextField(blank=True, null=True, help_text="Optional: Please pass the description of the product.")
    id_kategorii = models.ForeignKey('Kategoria', models.DO_NOTHING, db_column='id_kategorii', help_text="Please select the category of the product.")
    id_producenta = models.ForeignKey('Producent', models.DO_NOTHING, db_column='id_producenta', help_text="Please select the producer of the producer.")

    class Meta:
        managed = False
        db_table = 'produkty'
        ordering = ['nazwa']
    
    def __str__(self):
        return self.nazwa


class DostarczonyTowar(models.Model):
    data = models.DateField(default=timezone.now, help_text="Please pass the date of the delivery in YYYY-MM-DD format.")
    ilosc = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Please pass the quantity of the delivered items.")
    cena_jednostkowa_zakupu = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit purchase price of the delivered items.")
    cena_jednostkowa_sprzedazy = models.FloatField(validators=[MinValueValidator(0)], help_text="Please pass the unit selling price of the delivered items.")
    id_produktu = models.ForeignKey('Produkt', models.DO_NOTHING, db_column='id_produktu', help_text="Please select the wholesaler of the delivered items.")
    id_hurtownii = models.ForeignKey('Hurtownia', models.DO_NOTHING, db_column='id_hurtownii', help_text="Please select the product that has been delivered.")

    class Meta:
        managed = False
        db_table = 'dostarczone_towary'
        unique_together = (('data', 'id_hurtownii', 'id_produktu'),)
        ordering = ['-data', '-ilosc']

    def __str__(self):
        name = ''
        if self.id_produktu and self.id_hurtownii:
            name = f'{self.data} {self.id_produktu} from {self.id_hurtownii}'
        elif self.id_produktu and not self.id_hurtownii:
            name = f'{self.data} {self.id_produktu} from Unknown wholesaler'
        elif not self.id_produktu and self.id_hurtownii:
            name = f'{self.data} Unknown product from {self.id_hurtownii}'
        else:
            name = f'Unknown delivery {self.data}'
        
        available = self.ilosc
        items = PozycjaWZamowieniu.objects.filter(id_dostawy__id=self.id)
        for item in items:
            available -= item.ilosc_zamawiana
            
        return f'{name} ({available} left)'
    
    def save(self, *args, **kwargs):
        self.cena_jednostkowa_zakupu = round(self.cena_jednostkowa_zakupu, 2)
        self.cena_jednostkowa_sprzedazy = round(self.cena_jednostkowa_sprzedazy, 2)
        super().save(*args, **kwargs)


class Zamowienie(models.Model):
    numer = models.AutoField(primary_key=True)
    data_zlozenia = models.DateField(default=timezone.now, help_text="Please pass the date in YYYY-MM-DD format.")
    status = models.CharField(max_length=100, help_text="Please pass the status of the order.")
    komentarz = models.TextField(blank=True, null=True, help_text="Optional: Please add some comments.")
    id_adresu = models.ForeignKey('Adres', models.DO_NOTHING, db_column='id_adresu', help_text="Please choose the address.")
    id_klienta = models.ForeignKey('Klient', models.DO_NOTHING, db_column='id_klienta', help_text="Please select the client.")
    id_pracownika = models.ForeignKey('Pracownik', models.DO_NOTHING, db_column='id_pracownika', help_text="Please select the employee responsible for the order.")

    class Meta:
        managed = False
        db_table = 'zamowienia'
        ordering = ['-numer']
    
    def __str__(self):
        return f'#{self.numer} Status: {self.status}'


class PozycjaWZamowieniu(models.Model):
    ilosc_zamawiana = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Please define quantity of product.")
    id_dostawy = models.ForeignKey('DostarczonyTowar', models.DO_NOTHING, db_column='id_dostawy', help_text="Please select the delivery of the product.")
    numer_zamowienia = models.ForeignKey('Zamowienie', models.DO_NOTHING, db_column='numer_zamowienia')

    class Meta:
        managed = False
        db_table = 'pozycje_w_zamowieniach'
        unique_together = (('id_dostawy', 'numer_zamowienia'),)
        ordering = ['ilosc_zamawiana']
    
    def __str__(self):
        if not self.id_dostawy:
            return 'Unknown item'
        return f'{self.ilosc_zamawiana}x {self.id_dostawy.id_produktu} for {self.id_dostawy.cena_jednostkowa_sprzedazy} PLN'


class Platnosc(models.Model):
    data = models.DateTimeField(default=timezone.now, help_text="Please pass the date of the payment.")
    kwota = models.FloatField(validators=[MinValueValidator(0)],  help_text="Please pass the amount of the payment.")
    numer_zamowienia = models.ForeignKey('Zamowienie', models.DO_NOTHING, db_column='numer_zamowienia', help_text="Please select the order for which the payment was made.")

    class Meta:
        managed = False
        db_table = 'platnosci'
        unique_together = (('data', 'numer_zamowienia'),)
        ordering = ['-data']
    
    def __str__(self):
        if self.numer_zamowienia:
            return f'Payment #{self.id} for order #{self.numer_zamowienia.numer}'
        return f'Payment #{self.id}'

    def save(self, *args, **kwargs):
        self.kwota = round(self.kwota, 2)
        super().save(*args, **kwargs)
