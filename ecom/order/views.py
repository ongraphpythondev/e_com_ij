from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .serializers import CartSerializer


class CustomCartViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    This custom viewset is to only allow get and post method
    """
    pass



class CartViewSet(CustomCartViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return self.request.user.cart_set.all()