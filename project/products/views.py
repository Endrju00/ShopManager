from django.urls import reverse
from django.views import generic
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages


from .models import Category, DeliveredItems, Producer, Product, Wholesaler


class WholesalerListView(generic.ListView):
    model = Wholesaler
    paginate_by = 20
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Wholesalers'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class WholesalerDetailView(generic.DetailView):
    model = Wholesaler

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivered'] = DeliveredItems.objects.filter(
            wholesaler__id=self.kwargs['pk'])
        return context


class WholesalerCreateView(generic.edit.CreateView):
    model = Wholesaler
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was created successfully.')
        return reverse('products:wholesaler-detail', kwargs={'pk': self.object.id})


class WholesalerUpdateView(generic.edit.UpdateView):
    model = Wholesaler
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was updated successfully.')
        return reverse('products:wholesaler-detail', kwargs={'pk': self.object.id})


class WholesalerDeleteView(generic.edit.DeleteView):
    model = Wholesaler
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Wholesaler was deleted successfully.')
        return reverse('products:wholesaler-list')


class ProducerListView(generic.ListView):
    model = Producer
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Producers'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ProducerDetailView(generic.DetailView):
    model = Producer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            producer__name=self.kwargs['pk'])
        return context


class ProducerCreateView(generic.edit.CreateView):
    model = Producer
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was created successfully.')
        return reverse('products:producer-detail', kwargs={'pk': self.object.name})


class ProducerUpdateView(generic.edit.UpdateView):
    model = Producer
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was updated successfully.')
        return reverse('products:producer-detail', kwargs={'pk': self.object.name})


class ProducerDeleteView(generic.edit.DeleteView):
    model = Producer
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Producer was deleted successfully.')
        return reverse('products:producer-list')


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Categories'
        return context

    def get_queryset(self):
        queryset = Category.objects.filter(overcategory__isnull=True)
        return queryset

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': 'Categories',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = Category.objects.filter(
            overcategory__name=self.kwargs['pk'])
        context['products'] = Product.objects.filter(
            category__name=self.kwargs['pk'])
        return context


class CategoryCreateView(generic.edit.CreateView):
    model = Category
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was created successfully.')
        return reverse('products:category-detail', kwargs={'pk': self.object.name})


class CategoryUpdateView(generic.edit.UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was updated successfully.')
        return reverse('products:category-detail', kwargs={'pk': self.object.name})


class CategoryDeleteView(generic.edit.DeleteView):
    model = Category
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Category was deleted successfully.')
        return reverse('products:category-list')


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.model.__name__ + 's'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(generic.edit.CreateView):
    model = Product
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was created successfully.')
        return reverse('products:product-detail', kwargs={'pk': self.object.code})


class ProductUpdateView(generic.edit.UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was updated successfully.')
        return reverse('products:product-detail', kwargs={'pk': self.object.code})


class ProductDeleteView(generic.edit.DeleteView):
    model = Product
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Product was deleted successfully.')
        return reverse('products:product-list')


class DeliveredItemsListView(generic.ListView):
    model = DeliveredItems
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delivered Items'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(
                Q(date__contains=search) | Q(product__name__contains=search) | Q(wholesaler__name__contains=search)),
            'name': self.model.__name__,
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class DeliveredItemsDetailView(generic.DetailView):
    model = DeliveredItems


class DeliveredItemsCreateView(generic.edit.CreateView):
    model = DeliveredItems
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was created successfully.')
        return reverse('products:delivered-items-detail', kwargs={'pk': self.object.id})


class DeliveredItemsUpdateView(generic.edit.UpdateView):
    model = DeliveredItems
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was updated successfully.')
        return reverse('products:delivered-items-detail', kwargs={'pk': self.object.id})


class DeliveredItemsDeleteView(generic.edit.DeleteView):
    model = DeliveredItems
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Delivery was deleted successfully.')
        return reverse('products:delivered-items-list')
