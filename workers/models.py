from django.db import models
from django.contrib.auth.models import User
# Model for Customers (Users searching for workers)
class Customer(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # Store hashed password
    phone_number = models.CharField(max_length=15, unique=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

# Model for Workers (Service Providers)
class Worker(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # Store hashed password
    profession = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

# Model for Service Requests (Booking System)
class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requests')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='requests')
    service_type = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)