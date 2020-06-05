from django.urls import path
from . import views

urlpatterns = [
    path('self/', views.CurrentVendor.as_view(), name="vendor_self"),
    path('customers', views.ListCreateCustomers.as_view(), name="vendor_self"),
]