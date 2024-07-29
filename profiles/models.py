from django.db import models
from django.conf import settings
from orders.models import Layer  # Make sure to import the Layer model from the orders app
from users.models import CustomUser

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/funEmoji-1720771137510_44EkmhY.png')

    def __str__(self):
        return self.country # Assuming CustomUser has phone_number

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    amount_frozen = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    invitation_code = models.CharField(max_length=20, blank=True)
    daily_orders = models.IntegerField(default=38)
    commission_ratio = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    completed_orders = models.IntegerField(default=0)
    commision_earned=models.DecimalField(max_digits=10, decimal_places=3, default=0, null=True,blank=True)
    layer_information = models.ForeignKey(Layer, on_delete=models.SET_DEFAULT, default=1)  # Assuming Layer 0 has id=1

    def __str__(self) -> str:
        return self.phone_number

