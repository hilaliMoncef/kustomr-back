from django.db import models
from Customer.models import Customer
from Vendor.models import Vendor


class SMSCampaign(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="sms_campaigns")
    title = models.CharField(max_length=255)
    content = models.TextField()
    to = models.ManyToManyField(Customer, related_name="sms_campaigns")
    send_at = models.DateTimeField(null=True)
    sent = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "SMS Campaign by {} scheduled for {}".format(self.vendor.store_name, self.send_at)

    @property
    def length(self):
        return len(self.content)