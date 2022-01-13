from django.urls import path

from . import views


app_name = 'clients'
urlpatterns = [
    path('', views.ClientListView.as_view(), name='client-list'),
    path('report/', views.ClientReportView.as_view(), name='client-report'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('<int:pk>/update/', views.ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('create/', views.ClientCreateView.as_view(), name='client-create'),
]
