from rest_framework import serializers

from .models import Cart, CartItems
from account.api.serializers import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    item_cost = serializers.IntegerField(read_only=True)
    class Meta:
        model = CartItems
        exclude = ('id', 'cart')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_cost', 'timestamp', 'items', 'is_ordered')

        # read_only_fields = ['id',]

    def create(self, validated_data):
        request = self.context['request']
        cart_id = request.session.get('cart_id')
        
        cart, created = Cart.objects.get_or_create(pk=cart_id, user=request.user)
        
        request.session['cart_id'] = cart.pk

        for i in validated_data['items']:
            cart.add_item(**i)
        
        return cart
