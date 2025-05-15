from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('register/', views.register, name="register"),    # change to signup
    path('login/', views.custom_login, name="login"),  # change to login
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
    path('list-services/', views.list_services, name="list_services"),
    path('add-service/', views.add_service, name="add_service"),
    path('book-service/<int:service_id>/', views.book_service, name='book_service'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('provider-bookings/', views.home, name='pending_bookings'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('manage-bookings/', views.manage_bookings, name="manage_bookings"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('view-history/', views.view_history, name='view_history'),
    path('search-suggestions/', views.service_suggestions, name='service_suggestions'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/send/<str:receiver>/', views.send_message, name='send_message'),
    path('messages/send/<str:receiver>/<int:parent_id>/', views.send_message, name='reply_message'),
    path('messages/<int:message_id>/', views.view_message, name='view_message'),
    path('api/mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]