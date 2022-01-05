from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CartViewSet

router = DefaultRouter()
router.register('', CartViewSet, 'cart')

app_name = 'cart'

urlpatterns = [
    path('', include(router.urls)),
]