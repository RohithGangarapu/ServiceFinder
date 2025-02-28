from django.db import models
from django.contrib.auth.models import User

# Model for users who are finding workers (Customers)
class Customer(models.Model):
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255,default='pass')
    phone_number = models.CharField(max_length=15)
    latitude=models.FloatField(max_length=255,default=0.0)
    longitude=models.FloatField(max_length=255,default=0.0)   # Store address or coordinates

# Model for workers (e.g., plumbers, mechanics)
class Worker(models.Model):
    user = models. CharField(max_length=255)
    password = models.CharField(max_length=255,default='pass')
    profession = models.CharField(max_length=100)  # e.g., plumber, mechanic
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)  # Store address or coordinates
    latitude = models.FloatField()  # For map integration
    longitude = models.FloatField()  # For map integration
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

# Model for service requests
class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requests')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='requests')
    service_type = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Pending')  # e.g., Pending, Accepted, Completed
    created_at = models.DateTimeField(auto_now_add=True)
