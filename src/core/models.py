from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from ratings.models import Rating 

class Category(models.Model):
    Category_CHOICES=[
        ('salad', 'Salad'),
        ('sweet', 'Sweet'),
        ('sandwich', 'Sandwich'),
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('beverage', 'Beverage'),
        ('dessert', 'Dessert'),
        ('soup', 'Soup'),
    ]
    name=models.CharField(max_length=30,choices=Category_CHOICES)
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=20,unique=True)
    created_at=models.DateField(auto_now_add=True)
    ratings=GenericRelation(Rating)
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name
    
class RestaurantCategory(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('restaurant', 'category')





class Dish(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField()
    thumbnail=models.ImageField(upload_to='dish-img/',null=True)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    is_avalible=models.BooleanField(default=True)
    ratings = GenericRelation(Rating)


    class Meta:
        ordering = ['added_at']


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='customer')
    resturent=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address=models.TextField()
    phone=models.CharField(max_length=20,default="0000000000")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['created_at']



class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    dish=models.ForeignKey(Dish,on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'dish')




