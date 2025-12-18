from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User



class Rating(models.Model):
     Rating_TYPE=[
          ("dish","Dish"),
          ("resturent","Resturent"),
     ]
     score = models.PositiveSmallIntegerField()
     comment = models.TextField(blank=True)
     created_at=models.DateTimeField(auto_now_add=True)
     last_updated=models.DateTimeField(auto_now=True)
     user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
     type=models.CharField(max_length=10,choices= Rating_TYPE,null=True)
     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
     object_id = models.PositiveIntegerField()
     content_object = GenericForeignKey('content_type', 'object_id')


