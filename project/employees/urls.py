from django.urls import path

from . import views


app_name = 'employees'
urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employee-list'),
    path('report/', views.EmployeeReportView.as_view(), name='employee-report'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),

    path('positions/', views.PositionListView.as_view(), name='position-list'),
    path('positions/report/', views.PositionReportView.as_view(), name='position-report'),
    path('positions/create/', views.PositionCreateView.as_view(), name='position-create'),
    path('positions/<int:pk>/', views.PositionDetailView.as_view(), name='position-detail'),
    path('positions/<int:pk>/update/', views.PositionUpdateView.as_view(), name='position-update'),
    path('positions/<int:pk>/delete/', views.PositionDeleteView.as_view(), name='position-delete'),
]