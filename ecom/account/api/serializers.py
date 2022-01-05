from rest_framework import serializers
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
from account.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
       # fields = "__all__"
    
    def validate(self, attrs):
        print("here")
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user_without_password(phone = validated_data.get('phone'))
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone', 'first_login', 'is_admin')

class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    # password = serializers.CharField(
    #     style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        # password = attrs.get('password')

        if phone:
            if User.objects.filter(phone=phone).exists():
                user = User.objects.filter(phone=phone).first()
            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must Provide phone number.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

