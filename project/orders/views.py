from django.shortcuts import render
from django.views import generic

from .models import Address, ItemInOrder, Order, Payment


# Create your views here.
class AddressDetailView(generic.DetailView):
    model = Address


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 20
    template_name = 'list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Orders'
        return context


class OrderDetailView(generic.DetailView):
    model = Order


class ItemInOrderListView(generic.ListView):
    model = ItemInOrder
    paginate_by = 20
    template_name = 'list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Items in orders'
        return context
    
    # TODO Filter by order id


class ItemInOrderDetailView(generic.DeleteView):
    model = ItemInOrder


class PaymentListView(generic.ListView):
    model = Payment
    paginate_by = 20
    template_name = 'list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Payments'
        return context


class PaymentDetailView(generic.DetailView):
    model = Payment