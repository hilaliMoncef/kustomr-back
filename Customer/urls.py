from django.urls import path
from . import views

urlpatterns = [
    path('welcome/<int:pk>', views.LandingPageView.as_view(), name="customer_landing_page"),
    path('dashboard/<str:token>', views.DashboardView.as_view(), name="customer_home"),
    path('<int:pk>/transactions', views.CustomerTransactionList.as_view(), name="customer_transactions"),
]