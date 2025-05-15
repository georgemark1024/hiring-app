from django.contrib import admin
from .models import Service, Profile, Booking, Message
# Register your models here.
admin.site.register(Service)
admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(Message)

