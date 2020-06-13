from django import forms
from .models import EmailCampaign


class EmailCampaignForm(forms.ModelForm):
    class Meta:
        model = EmailCampaign
        exclude = ('mailjet_id',)
