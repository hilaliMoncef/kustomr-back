from rest_framework import serializers
from .models import SMSCampaign


class SMSCampaignSerializer(serializers.ModelSerializer):
    length = serializers.ReadOnlyField()
    
    class Meta:
        model = SMSCampaign
        fields = '__all__'