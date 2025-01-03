from django.urls import path
from .models import ProductDetailView
from .views import product_list, add_to_cart, cart_view, add_to_favorites, remove_from_favorites, favorites
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('add_to_favorites/<int:product_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', favorites, name='favorites'),
    path('products/', product_list, name='product_list'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)