from django.contrib import admin
from .models import Restaurant,Dish,Category

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Category)
