from django.shortcuts import render
from django.views import generic

from .models import Employee, Position


# Create your views here.
class EmployeeListView(generic.ListView):
    model = Employee
    paginate_by = 20
    template_name = 'list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Employees'
        return context


class EmployeeDetailView(generic.DetailView):
    model = Employee


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 20
    template_name = 'list.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Positions'
        return context


class PositionDetailView(generic.DetailView):
    model = Position
