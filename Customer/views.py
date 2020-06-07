from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from Vendor.models import Vendor
from .models import Customer, CustomerToken
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import CustomerForm
from django.utils.text import slugify
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from .serializers import CustomerSerializer, TransactionSerializer
from Vendor.serializers import VendorFullSerializer, ArticlesSerializer


class LandingPageView(APIView):
    """
    Cette vue permet de récupérer les principales stats sur le commerçant
    """
    def get(self, request, *args, **kwargs):
        vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
        if request.user.is_authenticated:
            return Response({'message': 'Vous êtes déjà connecté ailleurs.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(VendorFullSerializer(vendor).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'message': 'Vous êtes déjà connecté.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            vendor = get_object_or_404(Vendor, pk=self.kwargs['pk'])
            
            ## Here we check if a similar customer with the same email on the same store exists
            if vendor.customers.filter(email=request.data['email']).exists():
                return Response({'message': 'Un autre client est déjà inscrit avec la même adresse email.'}, status=status.HTTP_400_BAD_REQUEST)

            form = CustomerForm(data=request.data)
            if form.is_valid():
                customer = form.save(commit=False)
                customer.vendor = vendor
                customer.save()

                ## Add the logic for confirmation here
                current_site = get_current_site(request)
                mail_subject = 'Bienvenue chez {} !'.format(vendor.store_name)
                message = render_to_string('emails/register_confirmation.html', {
                    'customer': customer,
                    'domain': current_site.domain,
                    'vendor': vendor
                })
                to_email = customer.email
                send_mail(mail_subject, message, 'no-reply@app.kustomr.fr', [to_email], html_message=message, fail_silently=False)
                return Response({'vendor': vendor.pk, 'store_name': slugify(vendor.store_name), 'token': customer.token.token}, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response({'message': 'Une ou plusieurs erreurs se sont produites durant la validation du formulaire.'}, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    """
    Cette page permet d'afficher a tout detenteur du bon token son tableau de bord pour ce commerçant
    """
    def get(self, request,  *args, **kwargs):
        token = get_object_or_404(CustomerToken, token=self.kwargs['token'])
        customer = token.customer
        vendor = customer.vendor
        #discounts = list(vendor.discounts.filter(is_active=True, end_date__gte=timezone.now()))
        #offers = list(vendor.offers.filter(is_active=True, end_date__gte=timezone.now()))
        articles = vendor.articles.all()
        
        context = {
            'vendor': VendorFullSerializer(vendor).data,
            'customer': CustomerSerializer(customer).data,
            #'discounts': discounts + offers,
            'articles': ArticlesSerializer(articles, many=True).data
        }
        return Response(context, status=status.HTTP_200_OK)



class CustomerTransactionList(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        data = TransactionSerializer(customer.transactions, many=True).data
        return Response(data, status=status.HTTP_200_OK)