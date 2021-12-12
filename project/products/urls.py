from django.urls import path

from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),

    path('wholesalers/', views.WholeSalerListView.as_view(), name='wholesaler-list'),
    path('wholesalers/<int:pk>/', views.WholeSalerDetailView.as_view(), name='wholesaler-detail'),
    path('wholesalers/create/', views.WholesalerCreateView.as_view(), name='wholesaler-create'),

    path('producers/', views.ProducerListView.as_view(), name='producer-list'),
    path('producers/<int:pk>/', views.ProducerDetailView.as_view(), name='producer-detail'),
    path('producers/create/', views.ProducerCreateView.as_view(), name='producer-create'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),

    path('delivered-items/', views.DeliveredItemsListView.as_view(), name='delivered-items-list'),
    path('delivered-items/<int:pk>/', views.DeliveredItemsDetailView.as_view(), name='delivered-items-detail'),
    path('delivered-items/create/', views.DeliveredItemsCreateView.as_view(), name='delivered-items-create'),
]