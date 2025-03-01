from django.urls import path
from . import views

urlpatterns = [
    path('customer/register/', views.customer_register, name='customer_register'),
    path('worker/register/', views.worker_register, name='worker_register'),
    path('login/', views.user_login, name='login'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('search-workers/', views.search_workers, name='search_workers'),
     path('accept-order/<str:worker_username>/<str:customer_username>/<str:service_type>/', views.accept_order, name='accept_order'),
     path('book-worker/worker_name=<str:worker_name>/', views.book_worker, name='book_worker'),

]