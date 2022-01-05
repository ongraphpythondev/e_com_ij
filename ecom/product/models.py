from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    usage = models.CharField(max_length=150)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title   


    @property
    def is_active(self):
        return self.active



class Image(models.Model):
    caption = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return self.product.title
    