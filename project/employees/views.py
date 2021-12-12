from django.shortcuts import render
from django.views import generic

from .models import Employee, Position
from orders.models import Order

# Create your views here.
class EmployeeListView(generic.ListView):
    model = Employee
    paginate_by = 10
    template_name = 'employees/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Employees'
        return context


class EmployeeDetailView(generic.DetailView):
    model = Employee
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(employee__id=self.kwargs['pk'])
        return context


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 10
    template_name = 'employees/list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Positions'
        return context


class PositionDetailView(generic.DetailView):
    model = Position
