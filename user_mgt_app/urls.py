from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="user-landing"),
    path('register', views.register, name="user-register"),
    path('sign-up', views.sign_up, name="user-sign-in"),
]