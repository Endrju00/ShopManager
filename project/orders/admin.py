from django.contrib import admin

from .models import Address, ItemInOrder, Order, Payment

# Register your models here.
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(ItemInOrder)
admin.site.register(Payment)
