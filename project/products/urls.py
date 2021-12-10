from django.urls import path

from . import views

urlpatterns = [
    path('items/', views.ProductListView.as_view(), name='product-list'),
    path('items/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('wholesalers/', views.WholeSalerListView.as_view(), name='wholesaler-list'),
    path('wholesalers/<int:pk>/', views.WholeSalerDetailView.as_view(), name='wholesaler-detail'),
    path('producers/', views.ProducerListView.as_view(), name='producer-list'),
    path('producers/<int:pk>/', views.ProducerDetailView.as_view(), name='producer-detail'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('delivered-items/', views.DeliveredItemsListView.as_view(), name='delivered-items-list'),
    path('delivered-items/<int:pk>/', views.DeliveredItemsDetailView.as_view(), name='delivered-items-detail'),
]