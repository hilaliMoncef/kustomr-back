from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .forms import ArticleMediaUploadForm, VendorMediaUploadForm, DiscountMediaUploadForm
from .models import ArticleMedia, VendorMedia, DiscountMedia
from .serializers import VendorMediaSerializer, DiscountMediaSerializer, ArticleMediaSerializer



class DiscountUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = DiscountMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(DiscountMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)


class ArticleUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = ArticleMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(ArticleMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)


class VendorUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = VendorMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(VendorMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)