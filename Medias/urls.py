from django.urls import path
from . import views

urlpatterns = [
    path('vendors', views.VendorUploadView.as_view(), name="upload_vendors"),
    path('articles', views.ArticleUploadView.as_view(), name="upload_articles"),
    path('discounts', views.DiscountUploadView.as_view(), name="upload_discounts"),
    path('trainings', views.DiscountUploadView.as_view(), name="upload_trainings"),
    path('emails', views.EmailUploadView.as_view(), name="upload_emails"),
    path('socials', views.SocialUploadView.as_view(), name="upload_socials"),
]