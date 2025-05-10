from django.urls import path
from . import views

urlpatterns = [
    path('register/client/', views.register_client, name='register_client'),
    path('login/', views.user_login, name='login'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/psychologist/', views.psychologist_dashboard, name='psychologist_dashboard'),
    path('logout/', views.user_logout, name='logout'),
]