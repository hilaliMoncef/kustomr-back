from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .forms import ArticleMediaUploadForm, VendorMediaUploadForm, DiscountMediaUploadForm, TrainingMediaUploadForm, EmailMediaUploadForm, SocialMediaUploadForm
from .models import ArticleMedia, VendorMedia, DiscountMedia, TrainingMedia, EmailMedia, SocialMedia
from .serializers import VendorMediaSerializer, DiscountMediaSerializer, ArticleMediaSerializer, TrainingMediaSerializer, EmailMediaSerializer, SocialMediaSerializer



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


class TrainingUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = TrainingMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(TrainingMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)


class EmailUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = EmailMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(EmailMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)


class SocialUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        if request.FILES['file']:
            form = SocialMediaUploadForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                return Response(SocialMediaSerializer(image).data, status=status.HTTP_201_CREATED)
            else:
                print(form.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST)