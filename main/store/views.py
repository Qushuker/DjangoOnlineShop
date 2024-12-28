from django.shortcuts import render
from .models import Product, Category


def product_list(request):
    categorys = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products, 'categorys': categorys})