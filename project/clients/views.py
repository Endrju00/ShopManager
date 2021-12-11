from django.shortcuts import render
from django.views import generic

from .models import Client


# Create your views here.
class ClientListView(generic.ListView):
    model = Client
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Clients'
        return context


class ClientDetailView(generic.DetailView):
    model = Client
    