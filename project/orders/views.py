from django.urls import reverse
from django.views import generic

from .models import Address, ItemInOrder, Order, Payment


# Create your views here.
class AddressDetailView(generic.DetailView):
    model = Address


class AddressCreateView(generic.edit.CreateView):
    model = Address
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('orders:address-detail', kwargs={'pk': self.object.id})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Orders'
        return context


class OrderDetailView(generic.DetailView):
    model = Order

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = ItemInOrder.objects.filter(order__id=self.kwargs['pk'])
        context['payments'] = Payment.objects.filter(order__id=self.kwargs['pk'])
        return context


class OrderCreateView(generic.edit.CreateView):
    model = Order
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('orders:order-detail', kwargs={'pk': self.object.id})


class ItemInOrderListView(generic.ListView):
    model = ItemInOrder
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Items in orders'
        return context


class ItemInOrderDetailView(generic.DetailView):
    model = ItemInOrder


class PaymentListView(generic.ListView):
    model = Payment
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Payments'
        return context


class PaymentDetailView(generic.DetailView):
    model = Payment


class PaymentCreateView(generic.edit.CreateView):
    model = Payment
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('orders:payment-detail', kwargs={'pk': self.object.id})
