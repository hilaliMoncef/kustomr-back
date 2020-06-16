from django import forms
from .models import SMSCampaign


class SMSCampaignForm(forms.ModelForm):
    class Meta:
        model = SMSCampaign
        exclude = ('vendor',)
