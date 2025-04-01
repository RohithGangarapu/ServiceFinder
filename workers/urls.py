from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('customerregister', views.customer_register, name='customerregister'),
    path('workerregister', views.worker_register, name='workerregister'),
    path('workerdashboard/<str:worker>/', views.worker_dashboard, name='workerdashboard'),
    path('customerdashboard', views.customer_dashboard, name='customerdashboard'),
    path('book_worker', views.book_worker, name='book_worker'),
    path('acceptorder',views.accept_order,name='acceptorder')
    ]
