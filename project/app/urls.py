from django.urls import path

from . import views


app_name = 'app'
urlpatterns = [
    # PRODUCTS
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/report/', views.ProductReportView.as_view(), name='product-report'),
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'), 
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('products/wholesalers/', views.WholeSalerListView.as_view(), name='wholesaler-list'),
    path('products/wholesalers/report/', views.WholesalerReportView.as_view(), name='wholesaler-report'),
    path('products/wholesalers/create/', views.WholesalerCreateView.as_view(), name='wholesaler-create'),
    path('products/wholesalers/<int:pk>/', views.WholesalerDetailView.as_view(), name='wholesaler-detail'),
    path('products/wholesalers/<int:pk>/update/', views.WholesalerUpdateView.as_view(), name='wholesaler-update'),
    path('products/wholesalers/<int:pk>/delete/', views.WholesalerDeleteView.as_view(), name='wholesaler-delete'),

    path('products/producers/', views.ProducerListView.as_view(), name='producer-list'),
    path('products/producers/report/', views.ProducerReportView.as_view(), name='producer-report'),
    path('products/producers/create/', views.ProducerCreateView.as_view(), name='producer-create'),
    path('products/producers/<int:pk>/', views.ProducerDetailView.as_view(), name='producer-detail'),
    path('products/producers/<int:pk>/update/', views.ProducerUpdateView.as_view(), name='producer-update'),
    path('products/producers/<int:pk>/delete/', views.ProducerDeleteView.as_view(), name='producer-delete'),

    path('products/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('products/categories/report/', views.CategoryReportView.as_view(), name='category-report'),
    path('products/categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('products/categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('products/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('products/delivered-items/', views.DeliveredItemsListView.as_view(), name='delivered-items-list'),
    path('products/delivered-items/report/', views.DeliveredItemsReportView.as_view(), name='delivered-items-report'),
    path('products/delivered-items/create/', views.DeliveredItemsCreateView.as_view(), name='delivered-items-create'),
    path('products/delivered-items/<int:pk>/', views.DeliveredItemsDetailView.as_view(), name='delivered-items-detail'),
    path('products/delivered-items/<int:pk>/update/', views.DeliveredItemsUpdateView.as_view(), name='delivered-items-update'),
    path('products/delivered-items/<int:pk>/delete/', views.DeliveredItemsDeleteView.as_view(), name='delivered-items-delete'),

    # ORDERS
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/report/', views.OrderReportView.as_view(), name='order-report'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
    path('orders/<int:pk>/add/', views.AddItemView.as_view(), name='order-additem'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order-create'),

    path('orders/addresses/report/', views.AddressReportView.as_view(), name='address-report'),
    path('orders/addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    path('orders/addresses/<int:pk>/update/', views.AddressUpdateView.as_view(), name='address-update'),
    path('orders/addresses/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address-delete'),
    path('orders/addresses/create/', views.AddressCreateView.as_view(), name='address-create'),

    path('orders/items/', views.ItemInOrderListView.as_view(), name='items-list'),
    path('orders/items/report/', views.ItemInOrderReportView.as_view(), name='items-report'),
    path('orders/items/<int:pk>/', views.ItemInOrderDetailView.as_view(), name='items-detail'),
    path('orders/items/<int:pk>/update/', views.ItemInOrderUpdateView.as_view(), name='items-update'),
    path('orders/items/<int:pk>/delete/', views.ItemInOrderDeleteView.as_view(), name='items-delete'),
    path('orders/items/create/', views.ItemInOrderCreateView.as_view(), name='items-create'),

    path('orders/payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('orders/payments/report/', views.PaymentReportView.as_view(), name='payment-report'),
    path('orders/payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('orders/payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment-update'),
    path('orders/payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment-delete'),
    path('orders/payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),

    # EMPLOYEES
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/report/', views.EmployeeReportView.as_view(), name='employee-report'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee-create'),

    path('employees/positions/', views.PositionListView.as_view(), name='position-list'),
    path('employees/positions/report/', views.PositionReportView.as_view(), name='position-report'),
    path('employees/positions/create/', views.PositionCreateView.as_view(), name='position-create'),
    path('employees/positions/<int:pk>/', views.PositionDetailView.as_view(), name='position-detail'),
    path('employees/positions/<int:pk>/update/', views.PositionUpdateView.as_view(), name='position-update'),
    path('employees/positions/<int:pk>/delete/', views.PositionDeleteView.as_view(), name='position-delete'),

    # CLIENTS
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/report/', views.ClientReportView.as_view(), name='client-report'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client-update'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client-create'),
]
