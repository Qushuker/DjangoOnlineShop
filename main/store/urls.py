from django.urls import path
from .models import ProductDetailView
from .views import product_list

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

]