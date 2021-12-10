from django.shortcuts import render
from django.views import generic


# Create your views here.
from django.http import HttpResponse

from .models import Category, DeliveredItems, Producer, Product, Wholesaler


def index(request):
    return HttpResponse("Hello, world. You're at the products index.")


class WholeSalerListView(generic.ListView):
    model = Wholesaler
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Wholesalers'
        return context


class WholeSalerDetailView(generic.DetailView):

class ProducerListView(generic.ListView):
    model = Producer
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Producers'
        return context


class ProducerDetailView(generic.DetailView):

class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Categories'
        return context


class CategoryDetailView(generic.DetailView):

class ProductListView(generic.ListView):
    model = Product
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Products'
        return context


class ProductDetailView(generic.DetailView):

class DeliveredItemsListView(generic.ListView):
    model = DeliveredItems
    paginate_by = 20
    template_name = 'products/base_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delivered Items'
        return context


class DeliveredItemsDetailView(generic.DetailView):
