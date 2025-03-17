from django.shortcuts import render
from django.http import HttpResponse

def landing(request):
    return render(request, 'user_mgt_app/landing.html')

def register(request):
    return render(request, 'user_mgt_app/register.html')

def sign_in(request):
    return render(request, 'user_mgt_app/sign_in.html')
