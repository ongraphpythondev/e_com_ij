from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

from product.models import Product


User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        cart_short = f'{self.user.phone} : {self.updated_on}'
        return cart_short

    @property
    def cart_cost(self):
        total_cost = sum(item.product.cost*item.quantity for item in self.items.all())
        return total_cost

    @property
    def is_ordered(self):
        return hasattr(self, 'order')

    
    def add_item(self, product:Product, quantity:int):
        if product.is_active and type(quantity).__name__ == 'int' and not self.is_ordered:
            if quantity < 1:
                self.remove_item(product)
                return None

            item = self.items.update_or_create(product=product)[0]
            item.quantity = quantity
            item.save()
            return item
        return None

    def remove_item(self, product:Product):
        if not self.is_ordered:
            self.items.filter(product=product).delete()


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.product.title

    @property
    def item_cost(self):
        return self.product.cost




ORDER_STATUS = (
    ('0','placed'),
    ('1','packed'),
    ('2','dispatched'),
    ('3','on the way'),
    ('4','delivered'),
    ('5','canceled'),
    ('6','product returned'),
    ('7','product received'),
    ('8','refunded'),
)

STATUS_MAPPER = {
    0:'placed_on',
    1:'packed_on',
    2:'dispatch_on',
    3:'delivery_on',
    4:'delivered_on',
    5:'canceled_on',
    6:'returned_on',
    7:'received_on',
    8:'refunded_on',
}

PAYMENT_METHOD = (
    ('1', 'cash on delivery'),
    ('2', 'prepaid')
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='0')
    payment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD)
    placed_on = models.DateTimeField(auto_now_add=True)
    packed_on = models.DateField(null=True, blank=True)
    dispatch_on = models.DateField(null=True, blank=True)
    delivery_on = models.DateField(null=True, blank=True)
    delivered_on = models.DateField(null=True, blank=True)
    canceled_on = models.DateField(null=True, blank=True)
    returned_on = models.DateField(null=True, blank=True)
    received_on = models.DateField(null=True, blank=True)
    refunded_on = models.DateField(null=True, blank=True)



    def __str__(self):
        return self.cart.user.phone
    
    @property
    def current_status(self):
        return int(self.status)

    @property
    def is_placed(self):
        return self.placed_on

    @property
    def is_packed(self):
        return self.packed_on

    @property
    def is_dispatched(self):
        return self.dispatch_on

    @property
    def is_delivering(self):
        return self.delivery_on

    @property
    def is_delivered(self):
        return self.delivered_on

    @property
    def is_canceled(self):
        return self.canceled_on

    @property
    def is_returned(self):
        return self.returned_on

    @property
    def is_received(self):
        return self.received_on

    @property
    def is_refunded(self):
        return self.refunded_on


    def attr_parser(self, initial, end):
        l = dict(filter(lambda i: initial < i[0] <= end, STATUS_MAPPER.items()))
        return l.values()

    def change_status(self, status_code):
        if 1 <= status_code <= 8:
            temp_status = self.current_status

            if status_code < temp_status:
                l = self.attr_parser(status_code, temp_status)
                for item in l:
                    setattr(self, item, None)
            else:
                l = self.attr_parser(temp_status, status_code)
                for item in l:
                    setattr(self, item, datetime.today().date())
            self.status = str(status_code)
            self.save()
            return self

        return None