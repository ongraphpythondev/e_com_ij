from rest_framework.routers import DefaultRouter
from django.urls import path, include

from product.api.api import ProductViewSet

router = DefaultRouter()
router.register('', ProductViewSet, 'product')

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]