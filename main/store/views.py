from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Category, Color, Size, Cart, CartItem, FavoriteItem
from django.http import JsonResponse

#region Index

def index(request):
    
    return render(request, 'store/index.html')


def product_list(request):
    category_id = request.GET.get('category', '')
    color_id = request.GET.get('color', '')
    size_id = request.GET.get('size', '')
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    products = Product.objects.all()

    '''  Фильтры  '''
    if category_id:
        products = products.filter(category_id=category_id)
    if color_id:
        products = products.filter(color_id=color_id)
    if size_id:
        products = products.filter(size_id=size_id)

    '''  Сортировка  '''
    if order == 'desc':
        ''' Обратная '''
        products = products.order_by('-' + sort_by)
    else:
        '''Обычная'''
        products = products.order_by(sort_by)

    next_order = 'desc' if order == 'asc' else 'asc'

    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()



    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'colors': colors,
        'sizes': sizes,
        'sort_by': sort_by,
        'next_order': next_order,
        'category_id': category_id,
        'color_id': color_id,
        'size_id': size_id,
        #'total_items': total_items
    })

#endregion


#region Favorites

def favorites(request):
    favorite_items = FavoriteItem.objects.filter(user=request.user)
    products = [item.product for item in favorite_items]
    return render(request, 'store/favorites.html', {'products': products})


@csrf_exempt
def add_to_favorites(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        FavoriteItem.objects.get_or_create(user=request.user, product=product)
        return JsonResponse({'status': 'success'})

@csrf_exempt
def remove_from_favorites(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        FavoriteItem.objects.filter(user=request.user, product=product).delete()
        return JsonResponse({'status': 'success'})

def is_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_favorited = FavoriteItem.objects.filter(user=request.user, product=product).exists()
    return JsonResponse({'is_favorite': is_favorited})


#endregion

#region Cart

@login_required
def get_cart_item_quantity(request, product_id):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartitem = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        quantity = cartitem.quantity if cartitem else 0
        return JsonResponse({'quantity': quantity})
    else:
        return JsonResponse({'quantity': 0})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cartitem.quantity += 1
            cartitem.save()

        return JsonResponse({'success': True, 'quantity': cartitem.quantity})
    else:
        return JsonResponse({'success': False}, status=400)


def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_cost = 0
    if cart:
        for item in cart.cartitem_set.all():
            total_cost += item.product.price * item.quantity
    return render(request, 'store/cart.html', {'cart': cart, 'total_cost': total_cost})


@login_required
def increase_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cartitem = get_object_or_404(CartItem, cart=cart, product__id=product_id)
    cartitem.quantity += 1
    cartitem.save()
    return redirect('cart_view')


@login_required
def decrease_quantity(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cartitem = get_object_or_404(CartItem, cart=cart, product__id=product_id)

    if cartitem.quantity > 1:
        cartitem.quantity -= 1
        cartitem.save()
    else:
        cartitem.delete()  # Удаляем элемент, если количество 1
    return redirect('cart_view')


@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    try:
        cartitem = CartItem.objects.get(cart=cart, product__id=product_id)
        cartitem.delete()  # Удаляем элемент из корзины
    except CartItem.DoesNotExist:
        # Обработка случая, когда элемент не найден в корзине
        pass
    return redirect('cart_view')


@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cartitem_set.all().delete()  # Удаляем все элементы из корзины
    return redirect('cart_view')


@login_required
def get_cart_total_items(request):
    try:
        cart = Cart.objects.get(user=request.user)
        total_items = sum(cartitem.quantity for cartitem in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        total_items = 0
    return JsonResponse({'total_items': total_items})



#endregion