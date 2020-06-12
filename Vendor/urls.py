from django.urls import path
from . import views

urlpatterns = [
    path('self/', views.CurrentVendor.as_view(), name="vendor_self"),
    path('<int:pk>/update', views.UpdateVendor.as_view(), name="vendor_update"),
    path('<int:pk>/layout/update', views.UpdateLayoutVendor.as_view(), name="vendor_layout_update"),
    path('<int:pk>/hours/update', views.UpdateHourVendor.as_view(), name="vendor_hours_update"),
    path('customers', views.ListCreateCustomers.as_view(), name="vendor_customers"),
    path('customers/lists', views.ListCreateCustomersList.as_view(), name="vendor_customers_lists"),
]