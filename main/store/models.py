import random

from django.contrib.auth.models import User
from django.db import models
from django.views.generic import DetailView
import uuid





class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True)

    def generate_sku(self):
        """Генерация уникального SKU из 8 цифр."""
        return str(random.randint(10000000, 99999999))

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_sku()  # Генерация уникального артикула
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartItem')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

