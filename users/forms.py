from django import forms
from .models import Service

class UserTypeForm(forms.Form):
    USER_TYPES = [
        ('Client', 'Client'),
        ('ServiceProvider', 'Service Provider'),
        ('Both', 'Both'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.RadioSelect,
        label="Select your user type"
    )

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category', 'price', 'location', 'image', 'available']
