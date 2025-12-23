from django import forms
from core.models import RestaurantCategory

class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
     model=RestaurantCategory
     fields=['restaurant','category']
  
