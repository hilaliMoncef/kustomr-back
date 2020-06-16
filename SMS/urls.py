from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListSMSCampaigns.as_view(), name="sms"),
    path('new', views.AddSMSCampaign.as_view(), name="add_sms"),
]