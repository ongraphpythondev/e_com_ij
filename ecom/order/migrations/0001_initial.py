# Generated by Django 3.2.7 on 2022-01-04 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('0', 'placed'), ('1', 'packed'), ('2', 'dispatched'), ('3', 'on the way'), ('4', 'delivered'), ('5', 'canceled'), ('6', 'product returned'), ('7', 'product received'), ('8', 'refunded')], default='0', max_length=1)),
                ('payment_method', models.CharField(choices=[('1', 'cash on delivery'), ('2', 'prepaid')], max_length=1)),
                ('placed_on', models.DateTimeField(auto_now_add=True)),
                ('packed_on', models.DateField(blank=True, null=True)),
                ('dispatch_on', models.DateField(blank=True, null=True)),
                ('delivery_on', models.DateField(blank=True, null=True)),
                ('delivered_on', models.DateField(blank=True, null=True)),
                ('canceled_on', models.DateField(blank=True, null=True)),
                ('returned_on', models.DateField(blank=True, null=True)),
                ('received_on', models.DateField(blank=True, null=True)),
                ('refunded_on', models.DateField(blank=True, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
