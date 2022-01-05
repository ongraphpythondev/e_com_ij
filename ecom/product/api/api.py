from rest_framework.permissions import IsAdminUser, IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework import viewsets, response, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ProductImageSerializer
from product.models import Product, Image

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
   



