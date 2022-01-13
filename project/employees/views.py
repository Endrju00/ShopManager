from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db import connection
from django.contrib import messages

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
        context['search'] = 'Search for name/surname...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(Q(name__contains=search) | Q(surname__contains=search)),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class EmployeeReportView(generic.ListView):
    model = Employee
    template_name = 'employees/employee_report.html'


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
            if e.salary + 100 <= e.position.salary_max:
                with connection.cursor() as cursor:
                    cursor.execute(f"call podwyzka({self.kwargs['pk']}, 100)")
                    cursor.close()
                messages.add_message(self.request, messages.SUCCESS, 'An employee\'s salary has been increased by 100 PLN.')
            else:
                messages.add_message(self.request, messages.SUCCESS, 'It is impossible to raise an employee\'s salary any more.')
        context = {
            'object': Employee.objects.get(id=self.kwargs['pk']),
            'orders': Order.objects.filter(employee__id=self.kwargs['pk'])
        }

        return render(request, template_name='employees/employee_detail.html', context=context)


class EmployeeCreateView(generic.edit.CreateView):
    model = Employee
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was created successfully.')
        return reverse('employees:employee-detail', kwargs={'pk': self.object.id})


class EmployeeUpdateView(generic.edit.UpdateView):
    model = Employee
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was updated successfully.')
        return reverse('employees:employee-detail', kwargs={'pk': self.object.id})


class EmployeeDeleteView(generic.edit.DeleteView):
    model = Employee
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Employee was deleted successfully.')
        return reverse('employees:employee-list')


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10
    template_name = 'employees/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Positions'
        context['search'] = 'Search for the name...'
        return context

    def post(self, request, *args, **kwargs):
        search = self.request.POST.get('search')
        context = {
            'object_list': self.model.objects.filter(name__contains=search),
            'name': self.model.__name__ + 's',
            'results': f'Results for \"{search}\"'
        }
        return render(request, self.template_name, context=context)


class PositionReportView(generic.ListView):
    model = Position
    template_name = 'employees/position_report.html'


class PositionDetailView(generic.DetailView):
    model = Position

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.filter(
            position__id=self.kwargs['pk'])
        return context


class PositionCreateView(generic.edit.CreateView):
    model = Position
    template_name = 'create_form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was created successfully.')
        return reverse('employees:position-detail', kwargs={'pk': self.object.id})


class PositionUpdateView(generic.edit.UpdateView):
    model = Position
    fields = '__all__'
    template_name = 'update_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was updated successfully.')
        return reverse('employees:position-detail', kwargs={'pk': self.object.id})


class PositionDeleteView(generic.edit.DeleteView):
    model = Position
    template_name = 'delete_form.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Position was deleted successfully.')
        return reverse('employees:position-list')
