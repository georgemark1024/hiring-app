from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="user-landing"),
    path('register', views.register, name="user-register"),
    path('sign-in', views.sign_in, name="user-sign-in"),
]