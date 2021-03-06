from django.db import models
from Vendor.models import Vendor
from Customer.models import Customer
from Medias.models import EmailMedia


class EmailCampaign(models.Model):
    mailjet_id = models.CharField(max_length=255, null=True, blank=True)
    mailjet_custom_campaign = models.CharField(max_length=255, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="mail_campaigns")
    media = models.ForeignKey(EmailMedia, on_delete=models.SET_NULL, related_name="mail_campaigns", null=True, default=None)
    title = models.CharField(max_length=100)
    subject = models.TextField()
    content = models.TextField()
    to = models.ManyToManyField(Customer, related_name="mail_campaigns")
    isScheduled = models.BooleanField(default=False)
    send_at = models.DateField(default=None, null=True)
    sent = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Email Campaign by {} scheduled for {}".format(self.vendor.store_name, self.send_at)