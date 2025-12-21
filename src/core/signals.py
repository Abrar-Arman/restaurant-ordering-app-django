from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from .models import Dish


@receiver(post_delete,sender=Dish)
def delete_dish_thumbnail(sender, instance, **kwargs):
    print('test')
    if instance.thumbnail :
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

