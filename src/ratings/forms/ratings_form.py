from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ratings.models import Rating

class RestaurantRatingForm(forms.ModelForm):
    customer_id=forms.IntegerField(required=True)

    class Meta:
        model=Rating
        fields=['score','comment']
    
    def clean_score(self):
        score=self.cleaned_data.get('score')
        if score is not None:
           if score < 1 or score>5:
              raise  ValidationError("Score must be an integer between 0 and 5")
        return score
    
    def clean_customer_id(self):
        customer_id=self.cleaned_data.get("customer_id")
        try:
            User.objects.get(pk=customer_id)
        except User.DoesNotExist:
            raise ValidationError("Customer with this ID does not exist.")
        return customer_id
    

class RatingForm(forms.ModelForm):

    class Meta:
        model=Rating
        fields=['score','comment']
    
    def clean_score(self):
        score=self.cleaned_data.get('score')
        if score is not None:
           if score < 1 or score>5:
              raise  ValidationError("Score must be an integer between 0 and 5")
        return score
    
