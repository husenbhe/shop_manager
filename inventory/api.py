
from rest_framework import viewsets, permissions, decorators, response, status
from .models import Product, Sale
from .serializers import ProductSerializer, SaleSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = super().get_queryset()
        barcode = self.request.query_params.get('barcode')
        q = self.request.query_params.get('q')
        if barcode:
            qs = qs.filter(barcode=barcode)
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    @decorators.action(detail=False, methods=['get'])
    def lookup(self, request):
        barcode = request.query_params.get('barcode')
        if not barcode:
            return response.Response({'detail': 'barcode param required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(barcode=barcode)
            return response.Response(ProductSerializer(product).data)
        except Product.DoesNotExist:
            return response.Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related('product').all().order_by('-date')
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sale = serializer.save()
        product = sale.product
        product.stock = max(0, product.stock - sale.quantity)
        product.save()
