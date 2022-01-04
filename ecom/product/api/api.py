from rest_framework.permissions import IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import viewsets, response, mixins

from .serializers import ProductSerializer, ProductImageSerializer
from product.models import Product, Image

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
   



