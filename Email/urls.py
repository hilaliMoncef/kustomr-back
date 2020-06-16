from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListEmailCampaigns.as_view(), name="emails"),
    path('new', views.AddEmailCampaign.as_view(), name="add_email"),
    path('<int:pk>/statistics', views.StatisticsByEmailCampaign.as_view(), name="stat_email"),
    path('<int:pk>', views.RetrieveUpdateDestroyEmailCampaigns.as_view(), name="email"),
]