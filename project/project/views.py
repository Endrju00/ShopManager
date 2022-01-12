from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class ReportPageView(TemplateView):
    template_name = "report.html"
    

def error400Handler(request, exception):
    return render(request, 'error.html', context={'code': 400})

def error404Handler(request, exception):
    return render(request, 'error.html', context={'code': 404})

def error500Handler(request):
    return render(request, 'error.html', context={'code': 500})
