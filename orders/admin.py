from django.contrib import admin

from .models import Item, Order, Layer,OrderItem, WithdrawalRequest
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Layer)
admin.site.register(OrderItem)
admin.site.register(WithdrawalRequest)


