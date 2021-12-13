from django.urls import reverse
from django.views import generic

from .models import Client
from orders.models import Order

# Create your views here.
class ClientListView(generic.ListView):
    model = Client
    paginate_by = 10
    template_name = 'clients/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Clients'
        return context


class ClientDetailView(generic.DetailView):
    model = Client
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(employee__id=self.kwargs['pk'])
        return context


class ClientCreateView(generic.edit.CreateView):
    model = Client
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('clients:clients-detail', kwargs={'pk': self.object.id})


class ClientUpdateView(generic.edit.UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('clients:client-detail', kwargs={'pk': self.object.id})