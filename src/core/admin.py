from django.contrib import admin
from .models import Restaurant,Dish,Category,Order,OrderItem

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
