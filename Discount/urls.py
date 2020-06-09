from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListDiscounts.as_view(), name="discounts"),
    path('points', views.ListCreatePointsDiscounts.as_view(), name="points_discounts"),
    path('points/<int:pk>', views.RetrieveUpdateDestroyPointsDiscounts.as_view(), name="points_discount"),
    path('amount', views.ListCreateAmountDiscounts.as_view(), name="amount_discounts"),
    path('amount/<int:pk>', views.RetrieveUpdateDestroyAmountDiscounts.as_view(), name="amount_discount"),
    path('percent', views.ListCreatePercentDiscounts.as_view(), name="percent_discounts"),
    path('percent/<int:pk>', views.RetrieveUpdateDestroyPercentDiscounts.as_view(), name="percent_discount"),
]