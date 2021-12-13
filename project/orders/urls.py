from django.urls import path

from . import views


app_name = 'orders'
urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
    path('create/', views.OrderCreateView.as_view(), name='order-create'),

    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    path('addresses/<int:pk>/update/', views.AddressUpdateView.as_view(), name='address-update'),
    path('addresses/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address-delete'),
    path('addresses/create/', views.AddressCreateView.as_view(), name='address-create'),

    path('items/', views.ItemInOrderListView.as_view(), name='items-list'),
    path('items/<int:pk>/', views.ItemInOrderDetailView.as_view(), name='items-detail'),
    path('items/<int:pk>/update/', views.ItemInOrderUpdateView.as_view(), name='items-update'),
    path('items/<int:pk>/delete/', views.ItemInOrderDeleteView.as_view(), name='items-delete'),
    path('items/create/', views.ItemInOrderCreateView.as_view(), name='items-create'),

    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment-update'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment-delete'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),
]
