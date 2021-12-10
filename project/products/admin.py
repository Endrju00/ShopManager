from django.contrib import admin

from .models import Wholesaler, Producer, Category, Product, DeliveredItems

# Register your models here.
admin.site.register(Wholesaler)
admin.site.register(Producer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(DeliveredItems)
