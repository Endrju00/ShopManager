from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.db import connection
from django.http import HttpResponseRedirect

from .models import Address, ItemInOrder, Order, Payment


# Create your views here.
class AddressDetailView(generic.DetailView):
    model = Address


class AddressCreateView(generic.edit.CreateView):
    model = Address
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('orders:order-create')


class AddressUpdateView(generic.edit.UpdateView):
    model = Address
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('orders:address-detail', kwargs={'pk': self.object.id})


class AddressDeleteView(generic.edit.DeleteView):
    model = Address
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('orders:order-list')


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Orders'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(status__contains=search) | Q(client__name__contains=search) | Q(employee__name__contains=search) | Q(id__contains=search)),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


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
        return reverse('orders:items-create')


class OrderUpdateView(generic.edit.UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('orders:order-detail', kwargs={'pk': self.object.id})


class OrderDeleteView(generic.edit.DeleteView):
    model = Order
    template_name = 'delete_form.html'

    def get_success_url(self):
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
    fields = ['quantity', 'delivery']

    def get_success_url(self):
        if self.request.POST.get('first') == 'Add another one...':
            return reverse('orders:items-create')
        return reverse('orders:order-detail', kwargs={'pk': self.object.order.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.order = Order.objects.latest('id')
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ItemInOrderUpdateView(generic.edit.UpdateView):
    model = ItemInOrder
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('orders:items-detail', kwargs={'pk': self.object.id})


class ItemInOrderDeleteView(generic.edit.DeleteView):
    model = ItemInOrder
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('orders:order-list')


class PaymentListView(generic.ListView):
    model = Payment
    paginate_by = 10
    template_name = 'orders/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Payments'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(date__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class PaymentDetailView(generic.DetailView):
    model = Payment


class PaymentCreateView(generic.edit.CreateView):
    model = Payment
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('orders:payment-detail', kwargs={'pk': self.object.id})


class PaymentUpdateView(generic.edit.UpdateView):
    model = Payment
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('orders:payment-detail', kwargs={'pk': self.object.id})


class PaymentDeleteView(generic.edit.DeleteView):
    model = Payment
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('orders:payment-list')
