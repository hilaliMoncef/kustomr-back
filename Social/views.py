from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .models import FacebookPost
from .serializers import FacebookPostSerializer, FacebookPostSerializerLightSerializer


class ListCreateFacebookPost(generics.ListCreateAPIView):
    queryset = FacebookPost.objects.all()
    serializer_class = FacebookPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return FacebookPost.objects.order_by('-date_added')
        else:
            if user.is_vendor:
                # Vendor get only his customers
                return FacebookPost.objects.filter(vendor=user.vendor).order_by('-date_added')
            else:
                return FacebookPost.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return FacebookPostSerializerLightSerializer
        return FacebookPostSerializer