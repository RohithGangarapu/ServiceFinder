from django.shortcuts import render, redirect
from .models import Customer, Worker,ServiceRequest
from django.http import JsonResponse
# Registration View
def customer_register(request):
    if request.method == 'POST':
        
            # Create a customer profile
        Customer.objects.create(
        user=request.POST.get('username'),
        password=request.POST.get('password'),
        phone_number=request.POST.get('phone_number'),
        latitude=request.POST.get('latitude'),
        longitude=request.POST.get('longitude'))
        return redirect('customer_dashboard')
    return render(request, 'customer_register.html')

# Worker Registration View
def worker_register(request):
    if request.method == 'POST':
        # Create a user
        Worker.objects.create(
                user=request.POST.get('username'),
                password=request.POST.get('password'),
                profession=request.POST.get('profession'),
                phone_number=request.POST.get('phone_number'),
                location=request.POST.get('location'),
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'))
        return redirect('worker_dashboard')
    return render(request, 'worker_register.html')
# Login View
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Customer or Worker
        if user_type == 'customer':
                if Customer.objects.filter(user=username,password=password).exists():
                   return render(request, 'search_worker.html')
                else:
                    error = "You are not registered as a Customer."
        elif user_type == 'worker':
                if Worker.objects.filter(user=username,password=password).exists():
                    return redirect('worker_dashboard')
                else:
                    error = "You are not registered as a Worker."
        else:
            error = "Invalid username or password."
    return render(request, 'login.html', {'error': error})

# Home View with Role-Based Redirection
def home(request):
    if hasattr(request.user, 'customer'):
        return redirect('customer_dashboard')
    elif hasattr(request.user, 'worker'):
        return redirect('worker_dashboard')
    else:
        return redirect('admin_dashboard')  # For superusers

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
            'name': worker.user,
            'profession': worker.profession,
            'phone': worker.phone_number,
            'latitude': worker.latitude,
            'longitude': worker.longitude,
            'location': worker.location,
        }
        for worker in workers
    ]
    return JsonResponse(worker_data, safe=False)

def home(request):
    return render(request, 'search_workers.html')