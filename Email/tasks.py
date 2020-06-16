from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .models import EmailCampaign
from Medias.models import EmailMedia
from mailjet_rest import Client
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
import random
import os
import json


logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute=34, hour=13)),
    name="daily_email_campaigns",
    ignore_result=True
)
def daily_email_campaigns():
    """
    Send daily campaigns
    """
    campaigns = EmailCampaign.objects.filter(sent=False, send_at=timezone.now())
    for campaign in campaigns:
        api_key = settings.MJ_APIKEY_PUBLIC
        api_secret = settings.MJ_APIKEY_PRIVATE
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Building To dict
        to = []
        customers = campaign.to.all()
        
        # Rendering templates
        data = {}
        campaign_id = '{}-{}-{}'.format(campaign.vendor.pk, slugify(campaign.title), random.randint(0, 100000))
        data['Messages'] = []
        for customer in customers:
            template = render_to_string('emails/information_mail.html', {
                'customer': customer,
                'media': campaign.media,
                'content': campaign.content,
                'domain': 'app.kustomr.fr/',
                'vendor': campaign.vendor
            })

            message = {
                "From": {
                    "Email": "{}@kustomr.fr".format(slugify(campaign.vendor.store_name)),
                    "Name": campaign.vendor.store_name
                },
                "To": [{"Email": customer.email, "Name": customer.name}],
                "Subject": campaign.subject,
                "TextPart": strip_tags(campaign.content),
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
            logger.info("Sent campaign {}".format(campaign.pk))
        else:
            print(result.json())
            logger.info("Error in sending campaign to Mailjet")