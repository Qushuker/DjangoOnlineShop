from django.shortcuts import render, redirect
from .models import Product, Category, Color, Size


def product_list(request):
    category_id = request.GET.get('category')
    color_id = request.GET.get('color')
    size_id = request.GET.get('size')
    products = Product.objects.all()



    if category_id:
        products = products.filter(category_id=category_id)
    if color_id:
        products = products.filter(color_id=color_id)
    if size_id:
        products = products.filter(size_id=size_id)

    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    return render(request, 'store/product_list.html',
                  {'products': products, 'categories': categories, 'colors': colors, 'sizes': sizes})


