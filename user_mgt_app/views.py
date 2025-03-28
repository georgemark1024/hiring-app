from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.http import HttpResponse

def landing(request):
    return render(request, 'user_mgt_app/landing.html')

def register(request):
    return render(request, 'user_mgt_app/register.html')

def sign_in(request):
    return render(request, 'user_mgt_app/sign_in.html')

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