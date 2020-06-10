from django.db import models


class VendorMedia(models.Model):
    file = models.FileField(upload_to="vendors/")
    date_added = models.DateTimeField(auto_now_add=True)


class ArticleMedia(models.Model):
    file = models.FileField(upload_to="articles/")
    date_added = models.DateTimeField(auto_now_add=True)


class DiscountMedia(models.Model):
    file = models.FileField(upload_to="discounts/")
    date_added = models.DateTimeField(auto_now_add=True)


class TrainingMedia(models.Model):
    file = models.FileField(upload_to="trainings/")
    date_added = models.DateTimeField(auto_now_add=True)