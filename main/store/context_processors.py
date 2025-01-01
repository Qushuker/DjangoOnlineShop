from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        total_items = sum(cartitem.quantity for cartitem in cart.cartitem_set.all())
    else:
        total_items = 0
    return {'total_items': total_items}