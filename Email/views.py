from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from Customer.models import CustomersList, Customer
from Medias.models import EmailMedia
from .models import EmailCampaign
from .forms import EmailCampaignForm
from .serializers import EmailCampaignSerializer
from mailjet_rest import Client
from django.utils.text import slugify
from django.utils.html import strip_tags
import random
import os
import json


class ListEmailCampaigns(generics.ListAPIView):
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


class StatisticsByEmailCampaign(APIView):
    def get(self, request, pk, *args, **kwargs):
        campaign = get_object_or_404(EmailCampaign, pk=pk)

        api_key = settings.MJ_APIKEY_PUBLIC
        api_secret = settings.MJ_APIKEY_PRIVATE
        mailjet = Client(auth=(api_key, api_secret), version='v3')
        
        if not campaign.mailjet_id:
            result = mailjet.campaign.get(id=campaign.mailjet_custom_campaign)
            data = result.json()
            campaign.mailjet_id = data["Data"][0]["ID"]
            campaign.save()
        
        filters = {
            "ID": campaign.mailjet_id,
            "IDType": "Campaign"
        }
        result = mailjet.campaignoverview.get(filters=filters)
        data = result.json()["Data"][0]
        
        context = {
            'campaign': EmailCampaignSerializer(campaign).data,
            'stats': {
                "delivered": data["DeliveredCount"] / campaign.to.count(),
                "opened": data["OpenedCount"] / campaign.to.count(),
                "clicked": data["ClickedCount"] / campaign.to.count(),
            }
        }
        return Response(context, status=status.HTTP_200_OK)


class AddEmailCampaign(APIView):
    def post(self, request, *args, **kwargs):
        vendor = request.user.vendor

        form = EmailCampaignForm(request.data)

        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.vendor = vendor
            campaign.save()
            campaign.to.add(*request.data['to'])

            if not request.data['isScheduled']:
                # If campaign is immediate, we sent it right away

                api_key = settings.MJ_APIKEY_PUBLIC
                api_secret = settings.MJ_APIKEY_PRIVATE
                mailjet = Client(auth=(api_key, api_secret), version='v3.1')
                
                # Getting the used Media
                if request.data['media']:
                    media = get_object_or_404(EmailMedia, pk=request.data['media'])
                else:
                    media = None

                # Building To dict
                to = []
                customers = Customer.objects.filter(pk__in=request.data['to'])
                
                # Rendering templates
                data = {}
                campaign_id = '{}-{}-{}'.format(vendor.pk, slugify(request.data['title']), random.randint(0, 100000))
                data['Messages'] = []
                for customer in customers:
                    template = render_to_string('emails/information_mail.html', {
                        'customer': customer,
                        'media': media,
                        'content': request.data['content'],
                        'domain': 'app.kustomr.fr/',
                        'vendor': vendor
                    })

                    message = {
                        "From": {
                            "Email": "{}@kustomr.fr".format(slugify(vendor.store_name)),
                            "Name": vendor.store_name
                        },
                        "To": [{"Email": customer.email, "Name": customer.name}],
                        "Subject": request.data['subject'],
                        "TextPart": strip_tags(request.data['content']),
                        "HTMLPart": template,
                        "CustomCampaign": campaign_id,
                        "DeduplicateCampaign": True
                    }
                    
                    data['Messages'].append(message)

                result = mailjet.send.create(data=data)
                
                if result.status_code == 200:
                    campaign.mailjet_custom_campaign = campaign_id
                    campaign.sent = True
                    campaign.save()
                    return Response({'message': 'Votre campagne a bien été envoyée.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Une erreur s\'est produite lors de la programmation.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # The campaign is scheduled, Celery should take care of it.
                campaign.save()
                return Response({'message': 'Votre campagne a bien été programmée, elle sera envoyée à la date précisée.'}, status=status.HTTP_200_OK)
        else:
            print(form.errors)
            return Response({'message': 'Une erreur s\'est produite lors de la validation du formulaire.'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyEmailCampaigns(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAdminUser]