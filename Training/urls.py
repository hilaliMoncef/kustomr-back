from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListTrainings.as_view(), name="trainings"),
    path('add', views.CreateTrainings.as_view(), name="add_trainings"),
    path('<int:pk>', views.RetrieveUpdateDestroyTrainings.as_view(), name="training"),
]