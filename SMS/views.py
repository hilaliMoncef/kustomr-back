from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from Customer.models import Customer
from .models import SMSCampaign
from .forms import SMSCampaignForm
from .serializers import SMSCampaignSerializer
from django.utils.text import slugify
from django.conf import settings
from bitlyshortener import Shortener
import requests
import urllib
import sys
import os.path



class ListSMSCampaigns(generics.ListAPIView):
    queryset = SMSCampaign.objects.all()
    serializer_class = SMSCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SMSCampaign.objects.order_by('-date_added')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return SMSCampaign.objects.filter(vendor=user.vendor).order_by('-date_added')
            else:
                return SMSCampaign.objects.none()


class AddSMSCampaign(APIView):
    def post(self, request, *args, **kwargs):
        vendor = request.user.vendor

        form = SMSCampaignForm(request.data)

        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.vendor = vendor
            campaign.save()
            campaign.to.add(*request.data['to'])

            URL = 'https://api.smsmode.com/http/1.6/'
            PATH_SEND_SMS = "sendSMS.do"

            sms_sent = 0

            tokens_pool = ['890e64285cbb2d55b77c16a433feb3755b78de94']
            shortener = Shortener(tokens=tokens_pool, max_cache_size=8192)

            for customer in Customer.objects.filter(pk__in=request.data['to']):
                links = shortener.shorten_urls(['https://app.kustomr.fr/welcome/{}-{}/{}'.format(vendor.pk, slugify(vendor.store_name), customer.token.token)])
                final_url = (
                    URL + PATH_SEND_SMS +
                    '?accessToken=js0if6vjzu9KVjbW1kfPJtlQcPXnM27p' +
                    '&message=' + urllib.parse.quote_plus((request.data['content'] + '\nMon profil: {}'.format(links[0])).encode('iso-8859-15')) +
                    '&numero=' + customer.phone +
                    '&emetteur=' + slugify(vendor.store_name).replace('_', '').upper()[:11] +
                    '&stop=1'
                )
                r = requests.get(final_url)
                if r:
                    sms_sent += 1
            
            if sms_sent == 0:
                return Response({'message': 'Impossible de programmer la campagne SMS.'}, status=status.HTTP_400_BAD_REQUEST)
            campaign.sent = True
            campaign.save()
            return Response({'message': 'L\'envoi de {} SMS a été programmé.'.format(sms_sent)}, status=status.HTTP_200_OK)
        
        else:
            print(form.errors)
            return Response({'message': 'Impossible de valider le formulaire.'}, status=status.HTTP_400_BAD_REQUEST)