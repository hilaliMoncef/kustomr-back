from django.urls import path
from . import views

urlpatterns = [
    path('welcome/<int:pk>', views.LandingPageView.as_view(), name="customer_landing_page"),
    path('dashboard/<str:token>', views.DashboardView.as_view(), name="customer_home"),
    path('<int:pk>', views.RetrieveUpdateDestroyCustomer.as_view(), name="customer"),
    path('<int:pk>/transactions', views.CustomerTransactionList.as_view(), name="customer_transactions"),
    path('transactions', views.ListCreateTransactions.as_view(), name="vendor_transactions"),
    path('transactions/<int:pk>/refund', views.RefundTransaction.as_view(), name="vendor_refund_transactions"),
]