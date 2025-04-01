from django.shortcuts import render, redirect
from .models import Customer, Worker, ServiceRequest
import json
from django.http import JsonResponse
def home(request):
    return render(request,'home.html')
def register(request):
    return render(request,'register.html')
# Registration View
def customer_register(request):
    if request.method == 'POST':
        Customer.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            phone_number=request.POST.get('phone_number'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return redirect('login')
    return render(request, 'customerregister.html')
def book_worker(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            worker_id = data.get("worker_id")
            customer_name = data.get("customer_name")
            if not customer_name:
                return JsonResponse({"success": False, "error": "Customer name is required!"})
            # Create a service request entry with customer name
            ServiceRequest.objects.create(worker=Worker.objects.get(username=worker_id), customer=Customer.objects.get(username=customer_name), status="Pending")

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})
# Worker Registration View
def worker_register(request):
    if request.method == 'POST':
        worker = Worker.objects.create(
            username=request.POST.get('username'), 
            password=request.POST.get('password'),
            profession=request.POST.get('profession'),
            phone_number=request.POST.get('phone_number'),
            location=request.POST.get('location'),
            latitude=request.POST.get('latitude'),
            longitude=request.POST.get('longitude')
        )
        return redirect('login')
    return render(request, 'workerregister.html')

# Login View
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type') 
        if user_type == 'customer':
            if Customer.objects.filter(username=username,password=password).exists():
               return render(request,'customerdashboard.html',{'customer':username})  
        elif user_type == 'worker':
                if Worker.objects.filter(username=username,password=password).exists():
                   return redirect('workerdashboard',worker=username)  
    return render(request, 'login.html', {'error': error})

# Customer Dashboard View
def customer_dashboard(request):
    if 'customer' in request.GET:
         request.session['customer'] = request.GET['customer']
    customer = request.session.get('customer', '')
    profession_query = request.GET.get('profession', '').strip()
    workers = Worker.objects.filter(profession__icontains=profession_query)
    workers_list = list(workers.values("username", "latitude", "longitude", "profession", "location","phone_number"))
    return render(request, 'customerdashboard.html', {'workers': json.dumps(workers_list),'customer':customer})
# Worker Dashboard View
def worker_dashboard(request,worker):
    requests = ServiceRequest.objects.filter(worker=Worker.objects.get(username=worker))
    return render(request, 'workerdashboard.html', {'requests': requests})
def accept_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            worker = data.get("worker")
            customer=data.get("customer")
            # Find the service request and update status
            service_request = ServiceRequest.objects.get(worker=Worker.objects.get(username=worker),customer=Customer.objects.get(username=customer))
            service_request.status = "Accepted"
            service_request.save()

            return JsonResponse({"success": "Order accepted successfully!"}, status=200)

        except ServiceRequest.DoesNotExist:
            return JsonResponse({"error": "Service request not found!"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
