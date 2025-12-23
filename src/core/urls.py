from django.urls import path
from .views import get_categories,restaurants,restaurant_detail,manage_restaurant_category,create_dish,set_availability,dish_operation,create_order,change_order_status,manage_order,get_restaurant_orders,my_restaurants

urlpatterns = [
    path('categories/',get_categories,name='get-categories'),
    path('restaurants/',restaurants,name='get-create-resturent'),
    path('restaurants/my/',my_restaurants,name='my_restaurants'),
    path('restaurant/<int:pk>/',restaurant_detail,name='resturent-detail'),
    path('restaurant/<int:pk>/orders/',get_restaurant_orders,name='get_restaurant_orders'),
    path('restaurant/categories/',manage_restaurant_category,name='manage_restaurant_category'),
    path('dishes/',create_dish,name='create-dish'),
    path('dish/<int:pk>/',dish_operation,name='dish-operation'),
    path('dish/set-availability/',set_availability,name='dish-availability'),
    path('orders/',create_order,name='create_order'),
    path('order/<int:pk>/',manage_order,name='manage_order'),
    path('order/set-status/',change_order_status,name='change_order_status'),
]