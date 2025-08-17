
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import ProductViewSet, SaleViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'inventory'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='api-products')
router.register(r'sales', SaleViewSet, basename='api-sales')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('sales/add/', views.sale_create, name='sale_add'),
    path('scan/', views.scanner, name='scanner'),
    path('sales/<int:pk>/invoice.pdf', views.invoice_pdf, name='invoice_pdf'),
    # API + JWT
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
