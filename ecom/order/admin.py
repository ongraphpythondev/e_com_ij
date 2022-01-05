from django.contrib import admin

# Register your models here.


from .models import Order, CartItems, Cart

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItems)

