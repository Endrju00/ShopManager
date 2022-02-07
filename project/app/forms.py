from django import forms
from .models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['miasto'].label = 'City'
        self.fields['ulica'].label = 'Street'
        self.fields['nr_ulicy'].label = 'Street number'
        self.fields['kod_pocztowy'].label = 'Post code'
        self.fields['kraj'].label = 'Country'


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producent
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProducerForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].label = 'Name'
        self.fields['strona_www'].label = 'Website'


class WholesalerForm(forms.ModelForm):
    class Meta:
        model = Hurtownia
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(WholesalerForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].label = 'Name'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].label = 'Name'
        self.fields['id_nadkategorii'].label = 'Overcategory'


class ClientForm(forms.ModelForm):
    class Meta:
        model = Klient
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['imie'].label = 'Name'
        self.fields['nazwisko'].label = 'Surname'
        self.fields['nr_telefonu'].label = 'Phone number'
        self.fields['email'].label = 'Email'
        self.fields['kod_karty_rabatowej'].label = 'Discount card code'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Stanowisko
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.fields['nazwa'].label = 'Name'
        self.fields['placa_min'].label = 'Minimum salary'
        self.fields['placa_max'].label = 'Maximum salary'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Pracownik
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['imie'].label = 'Name'
        self.fields['nazwisko'].label = 'Surname'
        self.fields['nr_telefonu'].label = 'Phone number'
        self.fields['email'].label = 'Email'
        self.fields['placa'].label = 'Salary'
        self.fields['ilosc_godzin_tyg'].label = 'Number of hours per week'
        self.fields['id_stanowiska'].label = 'Position'

    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Produkt
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['kod'].label = 'Code'
        self.fields['nazwa'].label = 'Name'
        self.fields['opis'].label = 'Description'
        self.fields['id_kategorii'].label = 'Category'
        self.fields['id_producenta'].label = 'Producer'


class DeliveredItemsForm(forms.ModelForm):
    class Meta:
        model = DostarczonyTowar
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(DeliveredItemsForm, self).__init__(*args, **kwargs)
        self.fields['data'].label = 'Date'
        self.fields['ilosc'].label = 'Quantity'
        self.fields['cena_jednostkowa_zakupu'].label = 'Unit purchase price'
        self.fields['cena_jednostkowa_sprzedazy'].label = 'Unit selling price'
        self.fields['id_produktu'].label = 'Product'
        self.fields['id_hurtownii'].label = 'Wholesaler'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Zamowienie
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['data_zlozenia'].label = 'Date'
        self.fields['status'].label = 'Status'
        self.fields['komentarz'].label = 'Comment'
        self.fields['id_adresu'].label = 'Address'
        self.fields['id_klienta'].label = 'Client'
        self.fields['id_pracownika'].label = 'Employee'


class ItemInOrderForm(forms.ModelForm):
    class Meta:
        model = PozycjaWZamowieniu
        fields = ['ilosc_zamawiana', 'id_dostawy']

    def __init__(self, *args, **kwargs):
        super(ItemInOrderForm, self).__init__(*args, **kwargs)
        delivered = DostarczonyTowar.objects.all()
        wanted = set()

        for delivery in delivered:
            quantity = 0
            items = PozycjaWZamowieniu.objects.filter(id_dostawy__id=delivery.id)
            
            for item in items:
                quantity += item.ilosc_zamawiana
            
            if delivery.ilosc - quantity > 0:
                wanted.add(delivery.id)

        self.fields['id_dostawy'].queryset = DostarczonyTowar.objects.filter(id__in=wanted)
        self.fields['id_dostawy'].label = "Delivery"
        self.fields['ilosc_zamawiana'].label = "Quantity"


class ItemInOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = PozycjaWZamowieniu
        fields = ['ilosc_zamawiana', 'id_dostawy']

    def __init__(self, *args, **kwargs):
        super(ItemInOrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['id_dostawy'].label = "Delivery"
        self.fields['ilosc_zamawiana'].label = "Quantity"


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Platnosc
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['data'].label = 'Date'
        self.fields['kwota'].label = 'Amount'
        self.fields['numer_zamowienia'].label = 'Order'
