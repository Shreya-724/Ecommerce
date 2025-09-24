
from django.urls import path
from  . import views

from django.contrib import admin

urlpatterns = [
    path('success/', views.payment_success, name='payment_success'),
    path('khalti-payment/', views.khalti_payment, name="khalti_payment"),
    path('checkout', views.checkout, name='checkout'),
    
]