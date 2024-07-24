"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import shop.views as view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', view.ProductListView.as_view(), name='index'),
    path('products/', view.ProductListView.as_view(), name='products'),

    path('products/<int:pk>/', view.ProductDetailView.as_view(), name='product'),
    path('products/add_product/', view.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/edit/', view.ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', view.ProductDeleteView.as_view(), name='delete_product'),
    path('shopping_cart/', view.ShoppingCartListView.as_view(), name='shopping_cart'),
    path('shopping_cart/add/<int:pk>/', view.ShoppingCartAddProductView.as_view(), name='shopping_cart_create'),
    path('shopping_cart/delete/<int:pk>/', view.ShoppingCartProductDeleteView.as_view(), name='shopping_cart_delete'),
    path('shopping_cart/order/', view.OrderCreateView.as_view(), name='order')

]
