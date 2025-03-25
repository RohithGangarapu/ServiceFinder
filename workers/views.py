from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Worker, ServiceRequest
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Registration View
def customer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)  # Set password securely
        user.save()
        Customer.objects.create(
            user=user,
            password=password,
            phone_number=request.POST.get('phone_number'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return redirect('login')
    return render(request, 'customer_register.html')

# Worker Registration View
def worker_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)  
        user.save()

        worker = Worker.objects.create(
            user=user, 
            password=password,
            profession=request.POST.get('profession'),
            phone_number=request.POST.get('phone_number'),
            location=request.POST.get('location'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return redirect('login')
    return render(request, 'worker_register.html')

# Login View
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type') 

        user = authenticate(username=username, password=password)  

        if user is not None:
            login(request, user)  

            if user_type == 'customer':
                if Customer.objects.filter(user=user).exists():
                    return render(request, 'search_worker.html')  
                else:
                    error = "You are not registered as a Customer."
            elif user_type == 'worker':
                if Worker.objects.filter(user=user).exists():
                    return redirect('worker_dashboard')  
                else:
                    error = "You are not registered as a Worker."
            else:
                error = "Invalid user type selected."
        else:
            error = "Invalid username or password."

    return render(request, 'login.html', {'error': error})

# Customer Dashboard View
def customer_dashboard(request):
    workers = Worker.objects.filter(is_available=True)
    return render(request, 'customer_dashboard.html', {'workers': workers})

# Worker Dashboard View
def worker_dashboard(request):
    requests = ServiceRequest.objects.filter(worker__user=request.user)
    return render(request, 'worker_dashboard.html', {'requests': requests})

# Search for workers
def search_workers(request):
    profession = request.GET.get('profession', '')
    workers = Worker.objects.filter(profession__icontains=profession, is_available=True)
    
    worker_data = [
        {
            'name': worker.user.username,
            'profession': worker.profession,
            'phone': worker.phone_number,
            'latitude': worker.latitude,
            'longitude': worker.longitude,
            'location': worker.location,
        }
        for worker in workers
    ]
    return JsonResponse(worker_data, safe=False)

import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt # Only allow POST requests
def accept_order(request, worker_username, customer_username, service_type):
    try:
        worker = get_object_or_404(Worker, user__username=worker_username)
        customer = get_object_or_404(Customer, user__username=customer_username)

        # Normalize service_type to prevent case-sensitive mismatches
        service_request = get_object_or_404(
            ServiceRequest, 
            worker=worker, 
            customer=customer,
            service_type__iexact=service_type  # Case-insensitive match
        )
        
        if service_request.status == "Accepted":
            return JsonResponse({"message": "Order already accepted!"})

        service_request.status = "Accepted"
        service_request.save()

        return JsonResponse({"message": "Order Accepted!"})
    
    except Exception as e:
        logger.error(f"Error accepting order: {str(e)}")  # Log error for debugging
        return JsonResponse({"error": "An error occurred. Please try again."}, status=500)


# Book worker service
@csrf_exempt
def book_worker(request, worker_name):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User not authenticated"}, status=401)

        customer = get_object_or_404(Customer, user=request.user)
        worker = get_object_or_404(Worker, user__username=worker_name)

        service_request = ServiceRequest.objects.create(
            customer=customer,
            worker=worker,
            service_type="General Service",
            description="Customer requested a service",
            status="Pending"
        )

        return JsonResponse({"message": "Worker booked successfully!", "request_id": service_request.id})

    return JsonResponse({"message": "Invalid request"}, status=400)

# Update worker's live location
@csrf_exempt
def update_worker_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        try:
            worker = Worker.objects.get(user__username=username)
            worker.latitude = latitude
            worker.longitude = longitude
            worker.save()
            return JsonResponse({"message": "Location Updated!"})
        except Worker.DoesNotExist:
            return JsonResponse({"error": "Worker not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)

# Get all worker locations (for real-time tracking)

def get_worker_customer_location(request, worker_username):
    try:
        # Get logged-in user's username
        customer_username = request.user.username  

        # Fetch worker and customer based on usernames
        worker = get_object_or_404(Worker, user__username=worker_username)
        customer = get_object_or_404(Customer, user__username=customer_username)

        return JsonResponse({
            "worker_lat": worker.latitude,
            "worker_lon": worker.longitude,
            "customer_lat": customer.latitude,
            "customer_lon": customer.longitude
        })
    except Worker.DoesNotExist or Customer.DoesNotExist:
        return JsonResponse({"error": "Worker or Customer not found"}, status=404)