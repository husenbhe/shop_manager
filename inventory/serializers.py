
from rest_framework import serializers
from .models import Product, Sale

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'barcode', 'image', 'cost_price', 'selling_price', 'stock']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'product', 'quantity', 'date']
        read_only_fields = ['date']
