from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import UserTypeForm, ServiceForm
from .models import Service

def landing(request):
    return render(request, 'users/landing.html')

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
            return redirect('user_register')

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
    return render(request, 'users/select_user_type.html')

@login_required(login_url='user_sign_in')
def home(request):
    return render(request, "users/home.html")

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
    return render(request, 'users/sign_in.html')

@login_required(login_url='user_sign_in')
def user_logout(request):
    messages.success(request, "You have been logged out successfully.")
    logout(request)
    return redirect('user_landing')

@login_required(login_url='user_sign_in')
def select_user_type(request):
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user = request.user

            if user_type == 'Client':
                group = Group.objects.get(name='Client')
                user.groups.add(group)
            elif user_type == 'ServiceProvider':
                group = Group.objects.get(name='ServiceProvider')
                user.groups.add(group)
            elif user_type == 'Both':
                client_group = Group.objects.get(name='Client')
                provider_group = Group.objects.get(name='ServiceProvider')
                user.groups.add(client_group, provider_group)

            user.save()
            return redirect('home')

    else:
        form = UserTypeForm()

    return render(request, 'users/select_user_type.html', {'form': form})

@login_required(login_url='user_sign_in')
def search_services(request):
    query = request.GET.get('q')
    results = Service.objects.filter(name__icontains=query).order_by('-created_at')
    return render(request, 'users/search_results.html', {'results': results, 'query': query})

@login_required(login_url='user_sign_in')
def add_service(request):
    if not request.user.groups.filter(name="ServiceProvider").exists():
        return redirect('home')  # deny access for clients

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('list_services')
    else:
        form = ServiceForm()

    return render(request, 'users/add_service.html', {'form': form})

@login_required(login_url='user_sign_in')
def list_services(request):
    services = Service.objects.filter(available=True).order_by('-created_at')
    return render(request, 'users/list_services.html', {'services': services})

@login_required(login_url='user_sign_in')
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider=request.user)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('list_services')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'users/edit_service.html', {'form': form, 'service': service})

@login_required(login_url='user_sign_in')
def my_services(request):
    services = Service.objects.filter(provider=request.user)
    return render(request, 'users/my_services.html', {'services': services})
