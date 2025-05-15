from django import forms
from .models import Service, Profile, Message
from django.contrib.auth.models import User

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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'bio', 'location', 'profile_picture']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
        if sender:
            # Optional: exclude sender from choices
            self.fields['receiver'].queryset = User.objects.exclude(id=sender.id)

        if receiver:
            self.fields['receiver'].initial = receiver
            self.fields['receiver'].disabled = True