from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
     password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 8 characters."
    )

     class Meta:
        model=User
        fields=('password','email')
     def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters!")
        return password
   
