from django.urls import path

from . import views


app_name = 'orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    path('items/', views.ItemInOrderListView.as_view(), name='items-list'),
    path('items/<int:pk>/', views.ItemInOrderDetailView.as_view(), name='items-detail'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
]