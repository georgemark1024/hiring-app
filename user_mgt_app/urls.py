from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.landing, name="user-landing"),
    path('register/', views.register, name="user-register"),
    path('sign-in/', views.custom_login, name="user-sign-in"),
    path('home/', views.home, name="home"),
    # path('home/', TemplateView.as_view(template_name="user_mgt_app/home.html"), name="home")
]