from django.contrib import admin
from .models import Customer, Worker, ServiceRequest
admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(ServiceRequest)
# Register your models here.
