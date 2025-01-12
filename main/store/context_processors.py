from .models import Cart


def cartTotalCost(request):
    '''Количество товаров в корзине'''
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = sum(cartitem.quantity for cartitem in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            total_items = 0
    else:
        total_items = 0
    return {'total_items': total_items}
