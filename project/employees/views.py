from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db import connection

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

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(name__contains=search) | Q(surname__contains=search)),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class EmployeeDetailView(generic.DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            employee__id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('procedure'):
            e = Employee.objects.get(id=self.kwargs['pk'])
            if e.salary + 100 < e.position.salary_max:
                with connection.cursor() as cursor:
                    cursor.execute(f"call podwyzka({self.kwargs['pk']}, 100)")
                    cursor.close()

        context = {
            'object': Employee.objects.get(id=self.kwargs['pk'])
        }

        return render(request, template_name='employees/employee_detail.html', context=context)


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

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


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
