from django.urls import path
from .views import signup,login,logout,user_role

urlpatterns = [
   path('signup/',signup,name='signup'),
   path('login/',login,name='login'),
   path('logout/',logout,name='logout'),
   path('user-role/',user_role,name='user_role'),

]