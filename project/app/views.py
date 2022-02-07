from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import connection

from .models import *
from .forms import *

############################################################# PRODUKTY #################################################################

class WholeSalerListView(generic.ListView):
    model = Hurtownia
    paginate_by = 20
    template_name = 'app/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Wholesalers'
        context['search'] = 'Search for the name...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(nazwa__contains=search),
            'name': 'Wholesalers',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class WholesalerReportView(generic.ListView):
    model = Hurtownia
    template_name = 'app/wholesaler_report.html'


class WholesalerDetailView(generic.DetailView):
    model = Hurtownia
    template_name = 'app/wholesaler_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivered'] = DostarczonyTowar.objects.filter(
            id_hurtownii__id=self.kwargs['pk'])
        return context


class WholesalerCreateView(generic.edit.CreateView):
    model = Hurtownia
    template_name = 'create_form.html'
    form_class = WholesalerForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was created successfully.')
        return reverse('app:wholesaler-detail', kwargs={'pk': self.object.id})


class WholesalerUpdateView(generic.edit.UpdateView):
    model = Hurtownia
    form_class = WholesalerForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was updated successfully.')
        return reverse('app:wholesaler-detail', kwargs={'pk': self.object.id})


class WholesalerDeleteView(generic.edit.DeleteView):
    model = Hurtownia
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was deleted successfully.')
        return reverse('app:wholesaler-list')


class ProducerListView(generic.ListView):
    model = Producent
    paginate_by = 10
    template_name = 'app/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Producers'
        context['search'] = 'Search for the name...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(nazwa__contains=search),
            'name': 'Producers',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ProducerReportView(generic.ListView):
    model = Producent
    template_name = 'app/producer_report.html'


class ProducerDetailView(generic.DetailView):
    model = Producent
    template_name = 'app/producer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Produkt.objects.filter(
            id_producenta__id=self.kwargs['pk'])
        return context


class ProducerCreateView(generic.edit.CreateView):
    model = Producent
    template_name = 'create_form.html'
    form_class = ProducerForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was created successfully.')
        return reverse('app:producer-detail', kwargs={'pk': self.object.id})


class ProducerUpdateView(generic.edit.UpdateView):
    model = Producent
    form_class = ProducerForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was updated successfully.')
        return reverse('app:producer-detail', kwargs={'pk': self.object.id})


class ProducerDeleteView(generic.edit.DeleteView):
    model = Producent
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was deleted successfully.')
        return reverse('app:producer-list')


class CategoryListView(generic.ListView):
    model = Kategoria
    paginate_by = 10
    template_name = 'app/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Categories'
        context['search'] = 'Search for the name...'
        return context

    def get_queryset(self):
        queryset = Kategoria.objects.filter(id_nadkategorii__isnull=True)
        return queryset

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(nazwa__contains=search),
            'name': 'Categories',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class CategoryReportView(generic.ListView):
    model = Kategoria
    template_name = 'app/category_report.html'


class CategoryDetailView(generic.DetailView):
    model = Kategoria
    template_name = 'app/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = Kategoria.objects.filter(
            id_nadkategorii__id=self.kwargs['pk'])
        context['products'] = Produkt.objects.filter(
            id_kategorii__id=self.kwargs['pk'])
        return context


class CategoryCreateView(generic.edit.CreateView):
    model = Kategoria
    template_name = 'create_form.html'
    form_class = CategoryForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was created successfully.')
        return reverse('app:category-detail', kwargs={'pk': self.object.id})


class CategoryUpdateView(generic.edit.UpdateView):
    model = Kategoria
    form_class = CategoryForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was updated successfully.')
        return reverse('app:category-detail', kwargs={'pk': self.object.id})
    
    def get_failure_url(self):
        return reverse('app:category-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            if not self.object.id_nadkategorii:
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())

            category = self.object.id_nadkategorii
            categories = []

            while category:
                if category.id_nadkategorii:
                    categories.append(category.id_nadkategorii.nazwa)
                category = category.id_nadkategorii
            
            if self.object.id_nadkategorii.nazwa == self.object.nazwa or self.object.nazwa in categories:
                messages.add_message(
                    self.request, messages.SUCCESS,
                    f'WARNING: Changes were not applied. Define the overcategories correctly.')
                return HttpResponseRedirect(self.get_failure_url())
            else:
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())

        except Exception as e:
            print(str(e))
            messages.add_message(
                    self.request, messages.SUCCESS,
                    f'Something went wrong.')
            return HttpResponseRedirect(self.get_success_url())


class CategoryDeleteView(generic.edit.DeleteView):
    model = Kategoria
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was deleted successfully.')
        return reverse('app:category-list')


class ProductListView(generic.ListView):
    model = Produkt
    paginate_by = 10
    template_name = 'app/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Products'
        context['search'] = 'Search for the name...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(nazwa__contains=search),
            'name': 'Products',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ProductDetailView(generic.DetailView):
    model = Produkt
    template_name = 'app/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivered'] = DostarczonyTowar.objects.filter(
            id_produktu__id=self.kwargs['pk'])
        return context


class ProductCreateView(generic.edit.CreateView):
    model = Produkt
    template_name = 'create_form.html'
    form_class = ProductForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was created successfully.')
        return reverse('app:product-detail', kwargs={'pk': self.object.id})


class ProductUpdateView(generic.edit.UpdateView):
    model = Produkt
    form_class = ProductForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was updated successfully.')
        return reverse('app:product-detail', kwargs={'pk': self.object.id})


class ProductDeleteView(generic.edit.DeleteView):
    model = Produkt
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was deleted successfully.')
        return reverse('app:product-list')


class ProductReportView(generic.ListView):
    model = Produkt
    template_name = 'app/product_report.html'


class DeliveredItemsListView(generic.ListView):
    model = DostarczonyTowar
    paginate_by = 10
    template_name = 'app/products_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delivered Items'
        context['search'] = 'Search for date/product name/wholesaler...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(
                Q(data__contains=search) | Q(id_produktu__nazwa__contains=search) | Q(id_hurtownii__nazwa__contains=search)),
            'name': 'Delivered Items',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)

    
class DeliveredItemsReportView(generic.ListView):
    model = DostarczonyTowar
    template_name = 'app/delivereditems_report.html'


class DeliveredItemsDetailView(generic.DetailView):
    model = DostarczonyTowar
    template_name ='app/delivereditems_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = PozycjaWZamowieniu.objects.filter(id_dostawy__id=self.kwargs['pk'])
        return context


class DeliveredItemsCreateView(generic.edit.CreateView):
    model = DostarczonyTowar
    template_name = 'create_form.html'
    form_class = DeliveredItemsForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was created successfully.')
        return reverse('app:delivered-items-detail', kwargs={'pk': self.object.id})


class DeliveredItemsUpdateView(generic.edit.UpdateView):
    model = DostarczonyTowar
    form_class = DeliveredItemsForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was updated successfully.')
        return reverse('app:delivered-items-detail', kwargs={'pk': self.object.id})


class DeliveredItemsDeleteView(generic.edit.DeleteView):
    model = DostarczonyTowar
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was deleted successfully.')
        return reverse('app:delivered-items-list')


############################################################ ZAMOWIENIA ################################################################

class AddressReportView(generic.ListView):
    model = Adres
    template_name = 'app/address_report.html'


class AddressDetailView(generic.DetailView):
    model = Adres
    template_name = 'app/address_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Zamowienie.objects.filter(id_adresu__id=self.kwargs['pk'])
        return context


class AddressCreateView(generic.edit.CreateView):
    model = Adres
    template_name = 'create_form.html'
    form_class = AddressForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was created successfully.')
        return reverse('app:order-create')


class AddressUpdateView(generic.edit.UpdateView):
    model = Adres
    form_class = AddressForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was updated successfully.')
        return reverse('app:address-detail', kwargs={'pk': self.object.id})


class AddressDeleteView(generic.edit.DeleteView):
    model = Adres
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was deleted successfully.')
        return reverse('app:order-list')


class OrderListView(generic.ListView):
    model = Zamowienie
    paginate_by = 10
    template_name = 'app/orders_list.html'

    # def remove_empty_orders(self):
    #     orders = list(Order.objects.all())
    #     items = tuple(ItemInOrder.objects.all())
        
    #     # Remove orders that have items from the list
    #     for item in items:
    #         if item.order in orders:
    #             orders.remove(item.order)
        
    #     # Delete empty orders
    #     for order in orders:
    #         messages.add_message(self.request, messages.WARNING, f'Empty order deleted. (Order #{order.id}) ')
    #         order.delete()
            

    def get_context_data(self, **kwargs):
        # self.remove_empty_orders()  
        context = super().get_context_data(**kwargs)
        context['name'] = 'Orders'
        context['search'] = 'Search for status/client/employee/id...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(status__contains=search) | Q(id_klienta__imie__contains=search) | Q(id_pracownika__imie__contains=search) | Q(numer__contains=search)),
            'name': 'Orders',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class OrderReportView(generic.ListView):
    model = Zamowienie
    template_name = 'app/order_report.html'


class OrderDetailView(generic.DetailView):
    model = Zamowienie
    template_name = 'app/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = PozycjaWZamowieniu.objects.filter(
            numer_zamowienia__numer=self.kwargs['pk'])
        context['payments'] = Platnosc.objects.filter(
            numer_zamowienia__numer=self.kwargs['pk'])
        
        # funkcja
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CenaZamowienia ({self.kwargs['pk']})")
            data = cursor.fetchone()
            context['price'] = data
            cursor.close()
        return context


class OrderCreateView(generic.edit.CreateView):
    model = Zamowienie
    template_name = 'app/order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was created successfully.')
        return reverse('app:items-create')


class OrderUpdateView(generic.edit.UpdateView):
    model = Zamowienie
    form_class = OrderForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was updated successfully.')
        return reverse('app:order-detail', kwargs={'pk': self.object.numer})


class OrderDeleteView(generic.edit.DeleteView):
    model = Zamowienie
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was deleted successfully.')
        return reverse('app:order-list')


class ItemInOrderListView(generic.ListView):
    model = PozycjaWZamowieniu
    paginate_by = 10
    template_name = 'app/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Items in orders'
        return context


class ItemInOrderDetailView(generic.DetailView):
    model = PozycjaWZamowieniu
    template_name = 'app/iteminorder_detail.html'


class ItemInOrderCreateView(generic.edit.CreateView):
    model = PozycjaWZamowieniu
    template_name = 'app/item_create.html'
    form_class = ItemInOrderForm

    def get_success_url(self):
        if self.request.POST.get('first') == 'Add another one...':
            return reverse('app:items-create')
        return reverse('app:order-detail', kwargs={'pk': self.object.numer_zamowienia.numer})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.numer_zamowienia = Zamowienie.objects.latest('numer')

        items_in_order = PozycjaWZamowieniu.objects.filter(numer_zamowienia__numer=self.object.numer_zamowienia.numer)

        # Check if item is in the order already
        for item_in_order in items_in_order:
            if item_in_order.id_dostawy.id == self.object.id_dostawy.id:
                messages.add_message(
                        self.request, messages.SUCCESS,
                        f'WARNING: You can not add the same item to order. Use the quantity field in Item in order detail view.')
                        
                return HttpResponseRedirect(self.get_success_url())

        # Check availability
        available = self.object.id_dostawy.ilosc
        items = PozycjaWZamowieniu.objects.filter(id_dostawy=self.object.id_dostawy)
        for item in items:
            available -= item.ilosc_zamawiana

        if self.object.ilosc_zamawiana <= available:
            self.object.save()

        elif self.object.ilosc_zamawiana > available and available > 0:
            self.object.ilosc_zamawiana = available
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is not that much delivered items. Quantity set to {available}.')
            self.object.save()
            
        else:
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is no items in this delivery left. You can edit the order.')
        
        return HttpResponseRedirect(self.get_success_url())


class ItemInOrderReportView(generic.ListView):
    model = PozycjaWZamowieniu
    template_name = 'app/iteminorder_report.html'


class AddItemView(ItemInOrderCreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.numer_zamowienia = Zamowienie.objects.get(numer=self.kwargs['pk'])

        items_in_order = PozycjaWZamowieniu.objects.filter(numer_zamowienia__numer=self.object.numer_zamowienia.numer)
        
        # Check if item is in the order already
        for item_in_order in items_in_order:
            if item_in_order.id_dostawy.id == self.object.id_dostawy.id:
                messages.add_message(
                        self.request, messages.SUCCESS,
                        f'WARNING: You can not add the same item to order. Use the quantity field in Item in order detail view.')

                return HttpResponseRedirect(self.get_success_url())
        

        # Check availability
        available = self.object.id_dostawy.ilosc
        items = PozycjaWZamowieniu.objects.filter(id_dostawy=self.object.id_dostawy)

        for item in items:
            available -= item.ilosc_zamawiana

        if self.object.ilosc_zamawiana <= available:
            self.object.save()

        elif self.object.ilosc_zamawiana > available and available > 0:
            self.object.ilosc_zamawiana = available
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is not that much delivered items. Quantity set to {available}.')
            self.object.save()
            
        else:
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is no items in this delivery left. You can edit the order.')

        return HttpResponseRedirect(self.get_success_url())


class ItemInOrderUpdateView(generic.edit.UpdateView):
    model = PozycjaWZamowieniu
    form_class = ItemInOrderUpdateForm
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('app:items-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        old_quantity = PozycjaWZamowieniu.objects.get(id=self.object.id).ilosc_zamawiana
        old_obj = PozycjaWZamowieniu.objects.get(id=self.object.id)
        

        # Check availability
        if self.object.id_dostawy.id == old_obj.id_dostawy.id:
            available = self.object.id_dostawy.ilosc + old_quantity
            print("available")
        else:
            available = self.object.id_dostawy.ilosc

        items = PozycjaWZamowieniu.objects.filter(id_dostawy=self.object.id_dostawy)
        for item in items:
            available -= item.ilosc_zamawiana
        
        if self.object.ilosc_zamawiana <= available:
            self.object.save()

        elif self.object.ilosc_zamawiana > available and available > 0:
            self.object.ilosc_zamawiana = available
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is not that much delivered items. Quantity set to {available}.')
            self.object.save()
            
        else:
            messages.add_message(
                self.request, messages.SUCCESS,
                f'WARNING: There is no items in this delivery left. You can edit the order.')

        return HttpResponseRedirect(self.get_success_url())



class ItemInOrderDeleteView(generic.edit.DeleteView):
    model = PozycjaWZamowieniu
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Item was deleted successfully.')
        return reverse('app:order-list')


class PaymentListView(generic.ListView):
    model = Platnosc
    paginate_by = 10
    template_name = 'app/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Payments'
        context['search'] = 'Search for date...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(data__contains=search),
            'name': 'Payments',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class PaymentReportView(generic.ListView):
    model = Platnosc
    template_name = 'app/payment_report.html'
    

class PaymentDetailView(generic.DetailView):
    model = Platnosc
    template_name = 'app/payment_detail.html'


class PaymentCreateView(generic.edit.CreateView):
    model = Platnosc
    template_name = 'create_form.html'
    form_class = PaymentForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was created successfully.')
        return reverse('app:payment-detail', kwargs={'pk': self.object.id})


class PaymentUpdateView(generic.edit.UpdateView):
    model = Platnosc
    form_class = PaymentForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was updated successfully.')
        return reverse('app:payment-detail', kwargs={'pk': self.object.id})


class PaymentDeleteView(generic.edit.DeleteView):
    model = Platnosc
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was deleted successfully.')
        return reverse('app:payment-list')


############################################################ PRACOWNICY ################################################################

class EmployeeListView(generic.ListView):
    model = Pracownik
    paginate_by = 10
    template_name = 'app/employees_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Employees'
        context['search'] = 'Search for name/surname...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(imie__contains=search) | Q(nazwisko__contains=search)),
            'name': 'Employees',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class EmployeeReportView(generic.ListView):
    model = Pracownik
    template_name = 'app/employee_report.html'


class EmployeeDetailView(generic.DetailView):
    model = Pracownik
    template_name = 'app/employee_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Zamowienie.objects.filter(
            id_pracownika__id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('procedure'):
            e = Pracownik.objects.get(id=self.kwargs['pk'])

            # procedura 
            if e.placa + 100 <= e.id_stanowiska.placa_max:
                with connection.cursor() as cursor:
                    cursor.execute(f"call podwyzka({self.kwargs['pk']}, 100)")
                    cursor.close()
                messages.add_message(self.request, messages.SUCCESS, 'An employee\'s salary has been increased by 100 PLN.')
            else:
                messages.add_message(self.request, messages.SUCCESS, 'It is impossible to raise an employee\'s salary any more.')
                
        context = {
            'object': Pracownik.objects.get(id=self.kwargs['pk']),
            'orders': Zamowienie.objects.filter(id_pracownika__id=self.kwargs['pk'])
        }

        return render(request, template_name='app/employee_detail.html', context=context)


class EmployeeCreateView(generic.edit.CreateView):
    model = Pracownik
    template_name = 'create_form.html'
    form_class = EmployeeForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was created successfully.')
        return reverse('app:employee-detail', kwargs={'pk': self.object.id})


class EmployeeUpdateView(generic.edit.UpdateView):
    model = Pracownik
    form_class = EmployeeForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was updated successfully.')
        return reverse('app:employee-detail', kwargs={'pk': self.object.id})


class EmployeeDeleteView(generic.edit.DeleteView):
    model = Pracownik
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was deleted successfully.')
        return reverse('app:employee-list')


class PositionListView(generic.ListView):
    model = Stanowisko
    paginate_by = 10
    template_name = 'app/employees_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Positions'
        context['search'] = 'Search for the name...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(nazwa__contains=search),
            'name': 'Employees',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class PositionReportView(generic.ListView):
    model = Stanowisko
    template_name = 'app/position_report.html'


class PositionDetailView(generic.DetailView):
    model = Stanowisko
    template_name = 'app/position_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Pracownik.objects.filter(
            id_stanowiska__id=self.kwargs['pk'])
        return context


class PositionCreateView(generic.edit.CreateView):
    model = Stanowisko
    template_name = 'create_form.html'
    form_class = PositionForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was created successfully.')
        return reverse('app:position-detail', kwargs={'pk': self.object.id})


class PositionUpdateView(generic.edit.UpdateView):
    model = Stanowisko
    form_class = PositionForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was updated successfully.')
        return reverse('app:position-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=True)
        employees = Pracownik.objects.filter(id_stanowiska__id=self.object.id)
        
        for emp in employees:
            emp.placa = min(max(emp.placa, self.object.placa_min), self.object.placa_max)
            emp.save()

        return HttpResponseRedirect(self.get_success_url())

class PositionDeleteView(generic.edit.DeleteView):
    model = Stanowisko
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was deleted successfully.')
        return reverse('app:position-list')

############################################################# KLIENCI ##################################################################

class ClientListView(generic.ListView):
    model = Klient
    paginate_by = 10
    template_name = 'app/clients_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Clients'
        context['search'] = 'Search for name/surname...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(imie__contains=search) | Q(nazwisko__contains=search)),
            'name': 'Clients',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ClientReportView(generic.ListView):
    model = Klient
    template_name = 'app/client_report.html'


class ClientDetailView(generic.DetailView):
    model = Klient
    template_name = 'app/client_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Zamowienie.objects.filter(id_klienta__id=self.kwargs['pk'])
        return context


class ClientCreateView(generic.edit.CreateView):
    model = Klient
    template_name = 'create_form.html'
    form_class = ClientForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was created successfully.')
        return reverse('app:client-detail', kwargs={'pk': self.object.id})


class ClientUpdateView(generic.edit.UpdateView):
    model = Klient
    form_class = ClientForm
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was updated successfully.')
        return reverse('app:client-detail', kwargs={'pk': self.object.id})


class ClientDeleteView(generic.edit.DeleteView):
    model = Klient
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was deleted successfully.')
        return reverse('app:client-list')
