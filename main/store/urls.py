from django.urls import path
from .models import ProductDetailView
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('cart/', cart_view, name='cart_view'),

    path('get_cart_item_quantity/<int:product_id>/', get_cart_item_quantity, name='get_cart_item_quantity'),

    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('increase_quantity/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('api/cart/total-items/', get_cart_total_items, name='get_cart_total_items'),

    path('add_to_favorites/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', favorites, name='favorites'),
    path('is_favorite/<int:product_id>/', is_favorite, name='is_favorite'),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)