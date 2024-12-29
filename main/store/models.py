from django.db import models
from django.views.generic import DetailView





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



    def __str__(self):
        return self.name





class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


