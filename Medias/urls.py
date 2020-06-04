from django.urls import path
from . import views

urlpatterns = [
    path('self/', views.CurrentUser.as_view(), name="self_user"),
]