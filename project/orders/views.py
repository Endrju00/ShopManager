from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.db import connection
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.base import TemplateResponseMixin

from .models import Address, ItemInOrder, Order, Payment
from .forms import ItemInOrderForm


# Create your views here.
class AddressReportView(generic.ListView):
    model = Address
    template_name = 'orders/address_report.html'


class AddressDetailView(generic.DetailView):
    model = Address


class AddressCreateView(generic.edit.CreateView):
    model = Address
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was created successfully.')
        return reverse('orders:order-create')


class AddressUpdateView(generic.edit.UpdateView):
    model = Address
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was updated successfully.')
        return reverse('orders:address-detail', kwargs={'pk': self.object.id})


class AddressDeleteView(generic.edit.DeleteView):
    model = Address
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Address was deleted successfully.')
        return reverse('orders:order-list')


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10
    template_name = 'orders/list.html'

    def remove_empty_orders(self):
        orders = list(Order.objects.all())
        items = tuple(ItemInOrder.objects.all())
        
        # Remove orders that have items from the list
        for item in items:
            if item.order in orders:
                orders.remove(item.order)
        
        # Delete empty orders
        for order in orders:
            messages.add_message(self.request, messages.WARNING, f'Empty order deleted. (Order #{order.id}) ')
            order.delete()
            

    def get_context_data(self, **kwargs):
        self.remove_empty_orders()  
        context = super().get_context_data(**kwargs)
        context['name'] = 'Orders'
        context['search'] = 'Search for status/client/employee/id...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(status__contains=search) | Q(client__name__contains=search) | Q(employee__name__contains=search) | Q(id__contains=search)),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class OrderReportView(generic.ListView):
    model = Order
    template_name = 'orders/order_report.html'


class OrderDetailView(generic.DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = ItemInOrder.objects.filter(
            order__id=self.kwargs['pk'])
        context['payments'] = Payment.objects.filter(
            order__id=self.kwargs['pk'])
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT CenaZamowienia ({self.kwargs['pk']})")
            data = cursor.fetchone()
            context['price'] = data
            cursor.close()
        return context


class OrderCreateView(generic.edit.CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was created successfully.')
        return reverse('orders:items-create')


class OrderUpdateView(generic.edit.UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was updated successfully.')
        return reverse('orders:order-detail', kwargs={'pk': self.object.id})


class OrderDeleteView(generic.edit.DeleteView):
    model = Order
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Order was deleted successfully.')
        return reverse('orders:order-list')


class ItemInOrderListView(generic.ListView):
    model = ItemInOrder
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Items in orders'
        return context


class ItemInOrderDetailView(generic.DetailView):
    model = ItemInOrder


class ItemInOrderCreateView(generic.edit.CreateView):
    model = ItemInOrder
    template_name = 'orders/item_create.html'
    form_class = ItemInOrderForm

    def get_success_url(self):
        if self.request.POST.get('first') == 'Add another one...':
            return reverse('orders:items-create')
        return reverse('orders:order-detail', kwargs={'pk': self.object.order.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.order = Order.objects.latest('id')

        # Check availability
        available = self.object.delivery.quantity
        items = ItemInOrder.objects.filter(delivery=self.object.delivery)
        for item in items:
            available -= item.quantity

        if self.object.quantity <= available:
            self.object.save()

        elif self.object.quantity > available and available > 0:
            self.object.quantity = available
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
    model = ItemInOrder
    template_name = 'orders/iteminorder_report.html'


class AddItemView(ItemInOrderCreateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.order = Order.objects.get(id=self.kwargs['pk'])

        # Check availability
        available = self.object.delivery.quantity
        items = ItemInOrder.objects.filter(delivery=self.object.delivery)
        for item in items:
            available -= item.quantity

        if self.object.quantity <= available:
            self.object.save()

        elif self.object.quantity > available and available > 0:
            self.object.quantity = available
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
    model = ItemInOrder
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('orders:items-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        old_quantity = ItemInOrder.objects.get(id=self.object.id).quantity
        self.object = form.save(commit=False)

        # Check availability
        available = self.object.delivery.quantity + old_quantity
        items = ItemInOrder.objects.filter(delivery=self.object.delivery)
        for item in items:
            available -= item.quantity

        if self.object.quantity <= available:
            self.object.save()

        elif self.object.quantity > available and available > 0:
            self.object.quantity = available
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
    model = ItemInOrder
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Item was deleted successfully.')
        return reverse('orders:order-list')


class PaymentListView(generic.ListView):
    model = Payment
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Payments'
        context['search'] = 'Search for date...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(date__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class PaymentReportView(generic.ListView):
    model = Payment
    template_name = 'orders/payment_report.html'
    

class PaymentDetailView(generic.DetailView):
    model = Payment


class PaymentCreateView(generic.edit.CreateView):
    model = Payment
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was created successfully.')
        return reverse('orders:payment-detail', kwargs={'pk': self.object.id})


class PaymentUpdateView(generic.edit.UpdateView):
    model = Payment
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was updated successfully.')
        return reverse('orders:payment-detail', kwargs={'pk': self.object.id})


class PaymentDeleteView(generic.edit.DeleteView):
    model = Payment
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Payment was deleted successfully.')
        return reverse('orders:payment-list')
