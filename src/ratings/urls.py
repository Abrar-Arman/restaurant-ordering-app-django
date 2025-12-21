from django.urls import path
from .views import create_rating,manage_rating,user_ratings

urlpatterns = [
 path('restaurant/<int:pk>/rate/',create_rating,name='create_rating'),
 path('rating/<int:pk>/',manage_rating,name='manage_rating'),
 path('user/<int:pk>/ratings/',user_ratings,name='user_ratings'),

]