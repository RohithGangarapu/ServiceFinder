from django.shortcuts import render, redirect
from .models import Customer, Worker,ServiceRequest
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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
        longitude=request.POST.get('longitude'))
        return redirect('login')
    return render(request, 'customer_register.html')

# Worker Registration View
def worker_register(request):
    if request.method == 'POST':
        # Create a user
        username = request.POST.get('username')
        password = request.POST.get('password')

# Get or create the User instance
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)  # Set password securely
        user.save()

        # Create Worker instance with User instance
        worker = Worker.objects.create(
            user=user,  # Assign User instance instead of string
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
        user_type = request.POST.get('user_type')  # Customer or Worker

        user = authenticate(username=username, password=password)  # Django's authentication

        if user is not None:
            login(request, user)  # Log in the user

            # Check if the user is a customer or worker
            if user_type == 'customer':
                if Customer.objects.filter(user=user).exists():
                    return render(request, 'search_worker.html')  # Redirect to customer page
                else:
                    error = "You are not registered as a Customer."
            elif user_type == 'worker':
                if Worker.objects.filter(user=user).exists():
                    return redirect('worker_dashboard')  # Redirect to worker dashboard
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

def search_workers(request):
    profession = request.GET.get('profession', '')
    workers = Worker.objects.filter(profession__icontains=profession, is_available=True)
    
    # Convert worker data to JSON
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
def accept_order(request, worker_username, customer_username, service_type):
    try:
        # Find the worker by username
        worker = get_object_or_404(Worker, user=worker_username)

        # Find the service request uniquely identified by worker, customer, and service type
        service_request = get_object_or_404(
            ServiceRequest, 
            worker=worker.user.username, 
            customer=customer_username, 
            service_type=service_type
        )
        
        # Update the status to "Accepted"
        service_request.status = "Accepted"
        service_request.save()

        return JsonResponse({"message": "Order Accepted!"})
    
    except ServiceRequest.DoesNotExist:
        return JsonResponse({"error": "Service request not found"}, status=404)
    except Worker.DoesNotExist:
        return JsonResponse({"error": "Worker not found"}, status=404)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def book_worker(request, worker_name):
    if request.method == "POST":
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({"message": "User not authenticated"}, status=401)

        # Get the logged-in customer
        customer = get_object_or_404(Customer, user=request.user)

        # Get the worker instance by username
        worker = get_object_or_404(Worker, user__username=worker_name)

        # Create a service request
        service_request = ServiceRequest.objects.create(
            customer=customer,
            worker=worker,
            service_type="General Service",
            description="Customer requested a service",
            status="Pending"
        )

        return JsonResponse({"message": "Worker booked successfully!", "request_id": service_request.id})

    return JsonResponse({"message": "Invalid request"}, status=400)
