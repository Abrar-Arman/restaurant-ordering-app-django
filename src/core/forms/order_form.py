from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from core.models import Restaurant, Order, OrderItem, Dish


class OrderForm(forms.ModelForm):
    customer_id = forms.IntegerField(required=True)
    restaurant_id = forms.IntegerField(required=True)

    class Meta:
        model = Order
        fields = ['delivery_address', 'phone']

    def clean_customer_id(self):
        customer_id = self.cleaned_data.get('customer_id')
        try:
            User.objects.get(pk=customer_id)
        except User.DoesNotExist:
            raise ValidationError("Customer with this ID does not exist.")
        return customer_id

    def clean_restaurant_id(self):
        restaurant_id = self.cleaned_data.get('restaurant_id')
        try:
            Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise ValidationError("Restaurant with this ID does not exist.")
        return restaurant_id

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")
        return phone


class OrderItemForm(forms.ModelForm):
    dish_id = forms.IntegerField(required=True)

    class Meta:
        model = OrderItem
        fields = ['price', 'quantity']

    def clean_dish_id(self):
        dish_id = self.cleaned_data.get('dish_id')
        try:
            Dish.objects.get(pk=dish_id)
        except Dish.DoesNotExist:
            raise ValidationError("Dish does not exist.")
        return dish_id
    

class OrderStatusForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        error_messages={
            'invalid_choice': 'Invalid status. Choose from: confirmed, delivered, or cancelled.'
        }
    )


    class Meta:
        model=Order
        fields = ['status']
    def clean_status(self):
        status=self.cleaned_data.get('status')
        allowed_statuses = ['confirmed', 'delivered', 'cancelled']
        if status not in allowed_statuses:
            raise ValidationError(
                f"Invalid status '{status}'. Allowed values: {', '.join(allowed_statuses)}"
            )
        return status
    


class OrderUpdateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['delivery_address', 'phone']
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")
        return phone


       


     
                
        
           




