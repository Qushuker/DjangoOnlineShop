from django.urls import path
from .models import ProductDetailView
from .views import product_list, add_to_cart, cart_view

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view')

]