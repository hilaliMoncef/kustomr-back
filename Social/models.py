from django.db import models
from Medias.models import SocialMedia
from Vendor.models import Vendor


class FacebookPost(models.Model):
    facebook_id = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="facebook_posts")
    page_id = models.CharField(max_length=255)
    media = models.ForeignKey(SocialMedia, on_delete=models.SET_NULL, null=True, related_name="facebook_posts")
    content = models.TextField()
    send_at = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Facebook Post pour {} prévue pour {}'.format(self.vendor.store_name, self.send_at)
