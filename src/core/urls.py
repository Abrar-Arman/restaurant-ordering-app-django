from django.urls import path
from .views import restaurants,restaurant_detail,create_dish,set_availability,dish_operation,create_order,change_order_status,manage_order,get_restaurant_orders

urlpatterns = [
    path('restaurants/',restaurants,name='get-create-resturent'),
    path('restaurant/<int:pk>/',restaurant_detail,name='resturent-detail'),
    path('restaurant/<int:pk>/orders/',get_restaurant_orders,name='get_restaurant_orders'),
    path('dishes/',create_dish,name='create-dish'),
    path('dish/<int:pk>/',dish_operation,name='dish-operation'),
    path('dish/set-availability/',set_availability,name='dish-availability'),
    path('orders/',create_order,name='create_order'),
    path('order/<int:pk>/',manage_order,name='manage_order'),
    path('order/set-status/',change_order_status,name='change_order_status'),
]