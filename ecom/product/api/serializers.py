from rest_framework import serializers

from product.models import Product, Image

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = "__all__"
        extra_kwargs = {'product': {'write_only': True},}


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
   
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
      
        product_update = super().update(instance, validated_data)
        return product_update