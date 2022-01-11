from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages

from .models import Client
from orders.models import Order

# Create your views here.


class ClientListView(generic.ListView):
    model = Client
    paginate_by = 10
    template_name = 'clients/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Clients'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(name__contains=search) | Q(surname__contains=search)),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ClientDetailView(generic.DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            client__id=self.kwargs['pk'])
        return context


class ClientCreateView(generic.edit.CreateView):
    model = Client
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was created successfully.')
        return reverse('clients:client-detail', kwargs={'pk': self.object.id})


class ClientUpdateView(generic.edit.UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was updated successfully.')
        return reverse('clients:client-detail', kwargs={'pk': self.object.id})


class ClientDeleteView(generic.edit.DeleteView):
    model = Client
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Client was deleted successfully.')
        return reverse('clients:client-list')
