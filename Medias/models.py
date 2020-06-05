from django.db import models


class VendorMedia(models.Model):
    file = models.FileField(upload_to="vendors/")
    date_added = models.DateTimeField(auto_now_add=True)


class ArticleMedia(models.Model):
    file = models.FileField(upload_to="vendors/")
    date_added = models.DateTimeField(auto_now_add=True)