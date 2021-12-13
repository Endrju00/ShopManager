from django.urls import reverse
from django.views import generic

from .models import Employee, Position
from orders.models import Order

# Create your views here.


class EmployeeListView(generic.ListView):
    model = Employee
    paginate_by = 10
    template_name = 'employees/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Employees'
        return context


class EmployeeDetailView(generic.DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            employee__id=self.kwargs['pk'])
        return context


class EmployeeCreateView(generic.edit.CreateView):
    model = Employee
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('employees:employee-detail', kwargs={'pk': self.object.id})


class EmployeeUpdateView(generic.edit.UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('employees:employee-detail', kwargs={'pk': self.object.id})


class EmployeeDeleteView(generic.edit.DeleteView):
    model = Employee
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('employees:employee-list')


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10
    template_name = 'employees/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Positions'
        return context


class PositionDetailView(generic.DetailView):
    model = Position


class PositionCreateView(generic.edit.CreateView):
    model = Position
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('employees:position-detail', kwargs={'pk': self.object.id})


class PositionUpdateView(generic.edit.UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        return reverse('employees:position-detail', kwargs={'pk': self.object.id})


class PositionDeleteView(generic.edit.DeleteView):
    model = Position
    template_name = 'delete_form.html'

    def get_success_url(self):
        return reverse('employees:position-list')
