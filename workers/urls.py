from django.urls import path
from . import views

urlpatterns = [
    path('customer/register/', views.customer_register, name='customer_register'),
    path('worker/register/', views.worker_register, name='worker_register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('search-workers/', views.search_workers, name='search_workers'),
]