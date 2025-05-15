from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .forms import UserTypeForm, ServiceForm, UserForm, ProfileForm, MessageForm
from .models import Service, Booking, Message

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
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
            return redirect('register')

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
    return render(request, 'users/register.html')

@login_required(login_url='login')
def home(request):
    client_bookings = Booking.objects.filter(
        client=request.user,
        status='Pending'
    ).order_by('-booking_date')

    completed_bookings = Booking.objects.filter(
        client=request.user,
        status='Completed'
    ).order_by('-booking_date')

    pending_bookings = Booking.objects.filter(
        service__provider=request.user,
        status='Pending'
    ).order_by('-booking_date')

    accepted_bookings = Booking.objects.filter(
        service__provider=request.user,
        status='Accepted'  # Only show bookings waiting for action
    ).order_by('-booking_date')

    clients_accepted_bookings = Booking.objects.filter(
        client=request.user,
        status='Accepted'  # Only show bookings waiting for action
    ).order_by('-booking_date')

    return render(request, 'users/home.html',
                  {'client_bookings': client_bookings,
                   'completed_bookings': completed_bookings,
                   'pending_bookings': pending_bookings,
                   'accepted_bookings': accepted_bookings,
                   'clients_accepted_bookings': clients_accepted_bookings}
            )

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
    return render(request, 'users/login.html')

@login_required(login_url='login')
def user_logout(request):
    messages.success(request, "You have been logged out successfully.")
    logout(request)
    return redirect('landing')

@login_required(login_url='login')
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

@login_required(login_url='login')
def search_services(request):
    query = request.GET.get('q')

    if not query:
        # If no query, return to same page
        return redirect(request.META.get('HTTP_REFERER', '/'))

    results = Service.objects.filter(
        Q(name__icontains=query) |
        Q(category__icontains=query) |
        Q(provider__first_name__icontains=query) |
        Q(provider__last_name__icontains=query)
    ).order_by('-created_at')

    return render(request, 'users/search_results.html', {
        'results': results,
        'query': query
    })

@login_required(login_url='login')
def service_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        services = Service.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
        suggestions = list(services)

    return JsonResponse({'suggestions': suggestions})

@login_required(login_url='login')
def add_service(request):
    if not request.user.groups.filter(name="ServiceProvider").exists():
        return redirect('home')  # deny access for clients

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            return redirect('my_services')
    else:
        form = ServiceForm()

    return render(request, 'users/add_service.html', {'form': form})

@login_required(login_url='login')
def list_services(request):
    services = Service.objects.filter(available=True).order_by('-created_at')
    return render(request, 'users/list_services.html', {'services': services})

@login_required(login_url='login')
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

@login_required(login_url='login')
def my_services(request):
    services = Service.objects.filter(provider=request.user)
    return render(request, 'users/my_services.html', {'services': services})

@login_required(login_url='login')
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if service.provider == request.user:
        messages.warning(request, "You cannot book your own service.")
        return redirect('list_services')
    
    if request.method == 'POST':
        Booking.objects.create(
            client=request.user,
            service=service
        )
        return redirect('home')

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)

    if booking.status != 'Pending':
        messages.error(request, "You can only cancel bookings that are still pending.")
        return redirect('my_bookings')  # or your booking history/dashboard

    booking.status = 'Cancelled'
    booking.save()

    messages.success(request, f"Booking for {booking.service.name} has been cancelled.")
    return redirect('home')

@login_required(login_url='login')
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)

    if booking.status == 'Pending':
        booking.status = 'Accepted'
        booking.save()
        messages.success(request, "Booking accepted successfully.")
    else:
        messages.error(request, "Cannot accept a booking that is not pending.")

    return redirect('manage_bookings')


@login_required(login_url='login')
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, service__provider=request.user)

    if booking.status == 'Pending':
        booking.status = 'Rejected'
        booking.save()
        messages.success(request, "Booking rejected successfully.")
    else:
        messages.error(request, "Cannot reject a booking that is not pending.")

    return redirect('manage_bookings')

@login_required(login_url='login')
def manage_bookings(request):
    pending_bookings = Booking.objects.filter(
        service__provider=request.user,
        status='Pending'  # Only show bookings waiting for action
    ).order_by('-booking_date')

    accepted_bookings = Booking.objects.filter(
        service__provider=request.user,
        status='Accepted'  # Only show bookings waiting for action
    ).order_by('-booking_date')

    return render(request, "users/manage_bookings.html", {'pending_bookings': pending_bookings,
                                                          'accepted_bookings': accepted_bookings})

@login_required(login_url='login')
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')  # or wherever

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required(login_url='login')
def view_history(request):
    if request.user.groups.filter(name='Client').exists():
        completed_bookings = Booking.objects.filter(
            client = request.user,
            status = "Completed"
        ).order_by('-booking_date')
    elif request.user.groups.filter(name='ServiceProvider').exists():
        completed_bookings = Booking.objects.filter(
            service__provider = request.user,
            status = "Completed"
        ).order_by('-booking_date')

    return render(request, 'users/history.html', {
        'completed_bookings': completed_bookings,
    })

@login_required(login_url='login')
def send_message(request, receiver, parent_id=None):
    receiver_user = get_object_or_404(User, username=receiver)
    parent_message = None

    if parent_id:
        parent_message = get_object_or_404(Message, id=parent_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver_user
            if parent_message:
                message.parent = parent_message.parent if parent_message.parent else parent_message
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')
    else:
        form = MessageForm()

    return render(request, 'messages/send_message.html', {'form': form,
                                                          'receiver': receiver_user,
                                                          'parent': parent_message,
                                                          })

@login_required(login_url='login')
def inbox(request):
    messages = request.user.received_messages.order_by('-sent_at')
    return render(request, 'messages/inbox.html', {'inbox': messages})


@login_required(login_url='login')
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'messages/view_message.html', {'message': message})


logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            logger.info("M-Pesa Callback Received: %s", json.dumps(data, indent=2))

            stk_callback = data.get('Body', {}).get('stkCallback', {})
            merchant_request_id = stk_callback.get('MerchantRequestID')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')

            # Default values
            amount = receipt = phone = transaction_date = None

            # Only present if successful
            metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                name = item.get('Name')
                value = item.get('Value')
                if name == "Amount":
                    amount = value
                elif name == "MpesaReceiptNumber":
                    receipt = value
                elif name == "TransactionDate":
                    transaction_date = value
                elif name == "PhoneNumber":
                    phone = value

            # ✅ For now, just print both success and failure
            print("--- M-PESA TRANSACTION ---")
            print("MerchantRequestID:", merchant_request_id)
            print("CheckoutRequestID:", checkout_request_id)
            print("ResultCode:", result_code)
            print("ResultDesc:", result_desc)
            print("Amount:", amount)
            print("Receipt:", receipt)
            print("Phone:", phone)
            print("TransactionDate:", transaction_date)
            print("--------------------------")

            # TODO: Save to DB based on result_code

            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

        except Exception as e:
            logger.error("Callback Error: %s", str(e))
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Failed"})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)