from django.shortcuts import render
from django.views import generic

from .models import Client
from orders.models import Order

# Create your views here.
class ClientListView(generic.ListView):
    model = Client
    paginate_by = 20
    template_name = 'client_list.html'

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