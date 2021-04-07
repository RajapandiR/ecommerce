from django.contrib import admin

from ecomapp import models
# Register your models here.

admin.site.register(models.User1)
admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Shipping)