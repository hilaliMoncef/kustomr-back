from django.urls import path
from . import views

urlpatterns = [
    path('facebook', views.ListCreateFacebookPost.as_view(), name="facebook_posts"),
]