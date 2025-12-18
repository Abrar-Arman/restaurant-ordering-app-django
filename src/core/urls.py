from django.urls import path
from .views import restaurants,restaurant_detail,create_dish,set_availability,dish_operation
urlpatterns = [
    path('restaurants/',restaurants,name='get-create-resturent'),
    path('restaurant/<int:pk>/',restaurant_detail,name='resturent-detail'),
    path('dishes/',create_dish,name='create-dish'),
    path('dish/<int:pk>/',dish_operation,name='dish-operation'),
    path('dish/set-availability/',set_availability,name='dish-availability'),
]