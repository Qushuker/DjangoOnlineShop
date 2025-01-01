from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Product, Category, Color, Size, Cart, CartItem, FavoriteItem
from django.http import JsonResponse


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
    return render(request, 'store/product_list.html', {'products': products, 'categories': categories, 'colors': colors, 'sizes': sizes})

@login_required
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cartitem.quantity += 1
            cartitem.save()

        return redirect('cart_view')
    else:
        return redirect('login')


def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_cost = 0
    if cart:
        for item in cart.cartitem_set.all():
            total_cost += item.product.price * item.quantity
    return render(request, 'store/cart.html', {'cart': cart, 'total_cost': total_cost})


def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    FavoriteItem.objects.get_or_create(user=request.user, product=product)
    return redirect('favorites')

def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    FavoriteItem.objects.filter(user=request.user, product=product).delete()
    return redirect('favorites')

def favorites(request):
    favorite_items = FavoriteItem.objects.filter(user=request.user)
    products = [item.product for item in favorite_items]
    return render(request, 'store/favorites.html', {'products': products})