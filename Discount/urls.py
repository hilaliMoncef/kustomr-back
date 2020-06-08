from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListDiscounts.as_view(), name="discounts"),
    path('points', views.ListCreatePointsDiscounts.as_view(), name="points_discounts"),
    path('amount', views.ListCreateAmountDiscounts.as_view(), name="amount_discounts"),
    path('percent', views.ListCreatePercentDiscounts.as_view(), name="percent_discounts"),
]