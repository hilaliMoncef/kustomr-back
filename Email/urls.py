from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateEmailCampaigns.as_view(), name="emails"),
    path('new', views.AddEmailCampaign.as_view(), name="add_email"),
    path('statistics', views.StatisticsEmailCampaign.as_view(), name="add_email"),
    path('<int:pk>', views.RetrieveUpdateDestroyEmailCampaigns.as_view(), name="email"),
]