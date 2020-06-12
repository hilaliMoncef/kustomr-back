from django.db import models
from Vendor.models import Vendor
from Customer.models import Customer


class EmailCampaign(models.Model):
    mailjet_id = models.PositiveIntegerField(null=True, blank=True)
    mailjet_draft_id = models.PositiveIntegerField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="mail_campaigns")
    title = models.CharField(max_length=100)
    subject = models.TextField()
    content = models.TextField()
    to = models.ManyToManyField(Customer, related_name="mail_campaigns")
    template = models.CharField(max_length=255)
    send_at = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Email Campaign by {} scheduled for {}".format(self.vendor.store_name, self.send_at)