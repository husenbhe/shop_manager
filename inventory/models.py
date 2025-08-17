
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    barcode = models.CharField(max_length=64, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def is_low(self):
        return self.stock <= 5

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.selling_price * self.quantity

    def __str__(self):
        return f"Sale: {self.product.name} x {self.quantity} on {self.date:%Y-%m-%d}"
