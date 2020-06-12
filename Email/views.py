from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import EmailCampaign
from .serializers import EmailCampaignSerializer
from mailjet_rest import Client
from django.utils.text import slugify
from django.utils.html import strip_tags
import os


class ListCreateEmailCampaigns(generics.ListAPIView):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return EmailCampaign.objects.order_by('-date_added')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return EmailCampaign.objects.filter(vendor=user.vendor).order_by('-date_added')
            else:
                return EmailCampaign.objects.none()


class StatisticsEmailCampaign(APIView):
    def get(self, request, *args, **kwargs):
        api_key = '46a124dc7da2c21caf65a7fef536400c'
        api_secret = '0e37a3531511a7936b557dc02b757fe5'
        mailjet = Client(auth=(api_key, api_secret), version='v3')
        
        filters = {
            'IDType': 'Campaign',
            'ID': 7655003244
        }
        result = mailjet.campaignoverview.get(filters=filters)
        print(result.status_code)
        print(result.json())
        return Response(status=status.HTTP_200_OK)


class AddEmailCampaign(APIView):
    def post(self, request, *args, **kwargs):
        vendor = request.user.vendor
        api_key = '46a124dc7da2c21caf65a7fef536400c'
        api_secret = '0e37a3531511a7936b557dc02b757fe5'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "{}@kustomr.fr".format(slugify(vendor.store_name)),
                        "Name": vendor.store_name
                    },
                    "To": [
                        {
                            "Email": "hilali.moncef@gmail.com",
                            "Name": "Moncef"
                        }
                    ],
                    "Subject": request.data['subject'],
                    "TextPart": strip_tags(request.data['content']),
                    "HTMLPart": request.data['content'],
                    "CustomCampaign": request.data['name'],
                    "DeduplicateCampaign": True
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
        return Response(status=status.HTTP_200_OK)


class RetrieveUpdateDestroyEmailCampaigns(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAdminUser]