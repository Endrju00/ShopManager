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
    template_name = 'product_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Wholesalers'
        return context


class WholeSalerDetailView(generic.DetailView):
    model = Wholesaler

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['delivered'] = DeliveredItems.objects.filter(wholesaler__id=self.kwargs['pk'])
        return context


class ProducerListView(generic.ListView):
    model = Producer
    paginate_by = 10
    template_name = 'product_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Producers'
        return context


class ProducerDetailView(generic.DetailView):
    model = Producer
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(producer__id=self.kwargs['pk'])
        return context


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10
    template_name = 'product_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Categories'
        return context
    
    def get_queryset(self):
        queryset = Category.objects.filter(overcategory__isnull=True)
        return queryset

class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = Category.objects.filter(overcategory__id=self.kwargs['pk'])
        context['products'] = Product.objects.filter(category__id=self.kwargs['pk'])
        return context


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Products'
        return context


class ProductDetailView(generic.DetailView):
    model = Product


class DeliveredItemsListView(generic.ListView):
    model = DeliveredItems
    paginate_by = 10
    template_name = 'product_list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delivered Items'
        return context


class DeliveredItemsDetailView(generic.DetailView):
    model = DeliveredItems
