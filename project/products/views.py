from django.urls import reverse
from django.views import generic


from .models import Category, DeliveredItems, Producer, Product, Wholesaler


class WholesalerListView(generic.ListView):
    model = Wholesaler
    paginate_by = 20
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Wholesalers'
        return context


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
        return reverse('products:wholesaler-detail', kwargs={'pk': self.object.id})
        

class WholesalerUpdateView(generic.edit.UpdateView):
    model = DeliveredItems
    fields = '__all__'
    template_name = 'update_form.html'


class ProducerListView(generic.ListView):
    model = Producer
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Producers'
        return context


class ProducerDetailView(generic.DetailView):
    model = Producer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(
            producer__id=self.kwargs['pk'])
        return context


class ProducerCreateView(generic.edit.CreateView):
    model = Producer
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('products:producer-detail', kwargs={'pk': self.object.id})


class ProducerUpdateView(generic.edit.UpdateView):
    model = Producer
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('products:producer-detail', kwargs={'pk': self.object.id})


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


class CategoryDetailView(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subcategories'] = Category.objects.filter(
            overcategory__id=self.kwargs['pk'])
        context['products'] = Product.objects.filter(
            category__id=self.kwargs['pk'])
        return context


class CategoryCreateView(generic.edit.CreateView):
    model = Category
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('products:category-detail', kwargs={'pk': self.object.id})


class CategoryUpdateView(generic.edit.UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('products:category-detail', kwargs={'pk': self.object.id})


class ProductListView(generic.ListView):
    model = Product
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Products'
        return context


class ProductDetailView(generic.DetailView):
    model = Product


class ProductCreateView(generic.edit.CreateView):
    model = Product
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.object.code})


class ProductUpdateView(generic.edit.UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('products:product-detail', kwargs={'pk': self.object.code})


class DeliveredItemsListView(generic.ListView):
    model = DeliveredItems
    paginate_by = 10
    template_name = 'products/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Delivered Items'
        return context


class DeliveredItemsDetailView(generic.DetailView):
    model = DeliveredItems


class DeliveredItemsCreateView(generic.edit.CreateView):
    model = DeliveredItems
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('products:delivered-items-detail', kwargs={'pk': self.object.id})


class DeliveredItemsUpdateView(generic.edit.UpdateView):
    model = DeliveredItems
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('products:delivered-items-detail', kwargs={'pk': self.object.id})
