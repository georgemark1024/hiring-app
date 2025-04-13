from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name="user-landing"),
    path('register/', views.register, name="user-register"),    # change to signup
    path('sign-in/', views.custom_login, name="user-sign-in"),  # change to login
    path('home/', views.home, name="home"),
    path('about-us/', TemplateView.as_view(template_name="user_mgt_app/about_us.html"), name="about-us"),
    path('contact-us/', TemplateView.as_view(template_name="user_mgt_app/contact.html"), name="contact"),
    path('logout/', views.user_logout, name="user-logout"),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='user_mgt_app/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='user_mgt_app/password_change_done.html'), name='password_change_done'),

]