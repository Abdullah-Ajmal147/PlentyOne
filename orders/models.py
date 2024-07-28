from django.db import models
# from django.contrib.auth.models import User
from users.models import CustomUser



class Item(models.Model):
    item_id = models.AutoField(primary_key=True, verbose_name='Item ID')
    name = models.CharField(max_length=100, verbose_name='Name', blank=False, null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Unit Price', blank=False, null=False)
    order_quantity = models.IntegerField(verbose_name='Order Quantity', blank=False, null=False)
    product_image = models.ImageField(upload_to='products/images', default='default_image.jpg', verbose_name='Product Image')

    def __str__(self):
        return self.name

import string
import random

def generate_order_number():
    """Generates a random 6 character order number."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


class Layer(models.Model):
    level = models.PositiveIntegerField(unique=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    max_orders = models.PositiveIntegerField()
    commission = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return f"Layer {self.level}"

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FROZEN', 'Frozen'),
        ('COMPLETED', 'Completed'),
    ]
    order_no = models.CharField(max_length=20, unique=True, default=generate_order_number)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_commission = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    layer = models.ForeignKey(Layer, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only calculate commission for new orders
            self.calculate_commission()
        super().save(*args, **kwargs)

    def calculate_commission(self):
        user_orders_count = Order.objects.filter(user=self.user).count()
        eligible_layers = Layer.objects.filter(max_orders__gt=user_orders_count).order_by('-deposit')
        
        if eligible_layers.exists():
            self.layer = eligible_layers.first()
            self.order_commission = self.total * (self.layer.commission / 100)
        else:
            # Default to the lowest layer if no eligible layer is found
            default_layer = Layer.objects.order_by('deposit').first()
            self.layer = default_layer
            self.order_commission = self.total * (default_layer.commission / 100)

    def __str__(self):
        return f"Order {self.order_no}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in Order {self.order.order_no}"
