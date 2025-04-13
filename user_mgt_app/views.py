from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def landing(request):
    return render(request, 'user_mgt_app/landing.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('user-register')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Update profile info
            user.profile.phone = phone
            user.profile.save()

            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request, 'user_mgt_app/register.html')

@login_required(login_url='user-sign-in')
def home(request):
    return render(request, "user_mgt_app/home.html")

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'user_mgt_app/sign_in.html')

@login_required(login_url='user-sign-in')
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user-landing')