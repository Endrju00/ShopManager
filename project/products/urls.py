from django.urls import path

from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'), 
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'), path('create/', views.ProductCreateView.as_view(), name='product-create'),

    path('wholesalers/', views.WholesalerListView.as_view(), name='wholesaler-list'),
    path('wholesalers/<int:pk>/', views.WholesalerDetailView.as_view(),
         name='wholesaler-detail'),
    path('wholesalers/<int:pk>/update/',
         views.WholesalerUpdateView.as_view(), name='wholesaler-update'),
    path('wholesalers/<int:pk>/delete/',
         views.WholesalerDeleteView.as_view(), name='wholesaler-delete'),
    path('wholesalers/create/', views.WholesalerCreateView.as_view(),
         name='wholesaler-create'),

    path('producers/', views.ProducerListView.as_view(), name='producer-list'),
    path('producers/<int:pk>/', views.ProducerDetailView.as_view(), name='producer-detail'),
    path('producers/<int:pk>/update/', views.ProducerUpdateView.as_view(), name='producer-update'),
    path('producers/<int:pk>/delete/', views.ProducerDeleteView.as_view(), name='producer-delete'),
    path('producers/create/', views.ProducerCreateView.as_view(), name='producer-create'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),

    path('delivered-items/', views.DeliveredItemsListView.as_view(), name='delivered-items-list'),
    path('delivered-items/<int:pk>/', views.DeliveredItemsDetailView.as_view(), name='delivered-items-detail'),
    path('delivered-items/<int:pk>/update/', views.DeliveredItemsUpdateView.as_view(), name='delivered-items-update'),
    path('delivered-items/<int:pk>/delete/', views.DeliveredItemsDeleteView.as_view(), name='delivered-items-delete'),
    path('delivered-items/create/', views.DeliveredItemsCreateView.as_view(), name='delivered-items-create'),
]
