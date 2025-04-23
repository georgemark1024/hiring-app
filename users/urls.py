from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name="user_landing"),
    path('register/', views.register, name="user_register"),    # change to signup
    path('sign-in/', views.custom_login, name="user_sign_in"),  # change to login
    path('home/', views.home, name="home"),
    path('about-us/', TemplateView.as_view(template_name="users/about_us.html"), name="about_us"),
    path('contact-us/', TemplateView.as_view(template_name="users/contact.html"), name="contact"),
    path('logout/', views.user_logout, name="user-logout"),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('select-user-type', views.select_user_type, name="select_user_type"),
    path('search-services/', views.search_services, name="search_services"),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('my-services/', views.my_services, name="my_services"),

]